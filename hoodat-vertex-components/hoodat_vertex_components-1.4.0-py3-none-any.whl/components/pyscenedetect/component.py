from kfp.v2.dsl import component, Input, Output, Artifact, Dataset


@component(
    base_image="europe-west1-docker.pkg.dev/hoodat-sandbox/hoodat-sandbox-kfp-components/pyscenedetect",
    output_component_file="component.yaml",
)
def pyscenedetect(
    input_video: Input[Artifact],
    output_stats: Output[Dataset],
    output_scenes_df: Output[Dataset],
    output_video_dir: Output[Artifact],
    output_stats_path: str,
    output_scenes_df_path: str,
    output_video_dir_path: str,
    detector_threshold: float = 27.0,
):
    """Detects scenes in a video using PySceneDetect.

    Args:
        input_video (Input[Artifact]): The video to detect scenes in.
        output_stats (Output[Dataset]): A CSV file containing the stats of the scene detection.
        output_scenes_df (Output[Dataset]): A CSV file containing the start and end times of the detected scenes.
        output_video_dir (Output[Artifact]): A directory containing the video split into scenes.
        output_stats_path (str): The path to the output stats CSV file.
        output_scenes_df_path (str): The path to the output scenes CSV file.
        output_video_dir_path (str): The path to the output video directory.
        detector_threshold (float, optional): The threshold to use in the pyscenedetect ContentDetector. Defaults to 27.0.
    """
    import os
    import pandas as pd
    from scenedetect import open_video, SceneManager
    from scenedetect.detectors import ContentDetector
    from scenedetect.stats_manager import StatsManager
    from scenedetect.video_splitter import split_video_ffmpeg

    ################################
    # Helper functions
    ################################

    def setup_output_path(output_path):
        if output_path.startswith("gs://"):
            output_path_gs = output_path
            output_path_local = output_path.replace("gs://", "/gcs/")
        elif output_path.startswith("/gcs/"):
            output_path_gs = output_path.replace("/gcs/", "gs://")
            output_path_local = output_path
        else:
            raise ValueError("output_path should start with either gs:// or /gcs/")
        return output_path_gs, output_path_local

    def scenes_to_df(scene_list):
        df = pd.DataFrame(
            [
                {
                    "scene_number": i,
                    "start_frame": scene[0].frame_num,
                    "end_frame": scene[1].frame_num,
                    "start_time": str(scene[0]),
                    "end_time": str(scene[1]),
                }
                for i, scene in enumerate(scene_list)
            ]
        )
        return df

    ################################
    # Main
    ################################

    def split_video_into_scenes(
        video_path,
        output_stats_path,
        output_video_dir_path,
        output_scenes_df_path,
        threshold=detector_threshold,
    ):
        # Open the video, create a scene manager, and add a detector.
        video = open_video(video_path)
        stats_manager = StatsManager()
        # Construct the SceneManager and pass it the StatsManager.
        scene_manager = SceneManager(stats_manager)
        scene_manager.add_detector(ContentDetector(threshold=threshold))
        scene_manager.detect_scenes(video, show_progress=True)
        scene_list = scene_manager.get_scene_list()
        os.makedirs(os.path.dirname(output_stats_path), exist_ok=True)
        stats_manager.save_to_csv(
            csv_file=output_stats_path, base_timecode=None, force_save=True
        )
        os.makedirs(output_video_dir_path, exist_ok=True)
        split_video_ffmpeg(
            input_video_path=video_path,
            scene_list=scene_list,
            output_file_template=os.path.join(
                output_video_dir_path, "$VIDEO_NAME-Scene-$SCENE_NUMBER.mp4"
            ),
            show_progress=True,
        )
        os.makedirs(os.path.dirname(output_scenes_df_path), exist_ok=True)
        scenes_df = scenes_to_df(scene_list)
        scenes_df.to_csv(output_scenes_df_path, index=False)
        return scenes_df

    ################################
    # Setup output paths
    ################################

    output_path_stats_gs, output_path_stats_local = setup_output_path(output_stats_path)
    output_path_scenes_df_gs, output_path_scenes_df_local = setup_output_path(
        output_scenes_df_path
    )
    output_dir_video_gs, output_dir_video_local = setup_output_path(
        output_video_dir_path
    )
    output_stats.uri = output_path_stats_gs
    output_scenes_df.uri = output_path_scenes_df_gs
    output_video_dir.uri = output_dir_video_gs

    ################################
    # Run
    ################################

    split_video_into_scenes(
        video_path=input_video.path,
        output_stats_path=output_path_stats_local,
        output_scenes_df_path=output_path_scenes_df_local,
        output_video_dir_path=output_dir_video_local,
    )
