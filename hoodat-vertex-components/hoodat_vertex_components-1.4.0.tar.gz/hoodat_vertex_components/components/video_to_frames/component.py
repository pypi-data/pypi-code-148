from kfp.components import func_to_container_op


def video_to_frames_func(
    video_bucket: str, video_type: str, video_save_name: str, every_n_frames: int
):
    import os
    import cv2
    from math import floor

    # Read the video file
    source = f"/gcs/{video_bucket}/{video_type}/{video_save_name}"
    save_dir_root = f"/gcs/{video_bucket}/frames/{video_type}/{video_save_name}"
    if every_n_frames == 1:
        save_dir = f"{save_dir_root}/clean_complete/"
    elif every_n_frames == 30:
        save_dir = f"{save_dir_root}/clean/"
    else:
        raise
    vidcap = cv2.VideoCapture(source)
    vidcap_metrics = {
        "num_frames": int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)),
        "width": int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "height": int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        "fps": vidcap.get(cv2.CAP_PROP_FPS),
    }
    print(source)
    print(vidcap_metrics["num_frames"])
    print(vidcap_metrics["width"])
    print(vidcap_metrics["height"])
    print(vidcap_metrics["fps"])
    vidcap_metrics["num_frames_to_save"] = floor(
        float(vidcap_metrics["num_frames"]) / float(every_n_frames)
    )
    print("vidcap_metrics: " + str(vidcap_metrics))
    success, image = vidcap.read()
    print("Success: " + str(success))
    # Initialise the count that will increase with each frame
    count = 0
    # If the video is read successfully
    if success is True:
        save_dir_exists = os.path.isdir(save_dir)
        print("Directory already exists: " + str(save_dir_exists))
        if not save_dir_exists:
            os.makedirs(save_dir)
        frames_list = os.listdir(save_dir)
        if len(frames_list) == vidcap_metrics["num_frames"]:
            print("Frames already saved")
            success = False
        else:
            print("Saving output to: " + save_dir + "\n")
    while success:
        # Read the next frame
        try:
            success, image = vidcap.read()
            # Where to save the frame
            # if count % int(args.every_n_frames) == 0:
            if count % every_n_frames == 0:
                save_path = save_dir + "f" + str(count) + ".jpg"
                cv2.imwrite(save_path, image)  # save frame as JPEG file
            # Print progress after every 100th frame
            # if count % (int(args.every_n_frames) * 100) == 0:
            if count % (every_n_frames * 100) == 0:
                print("Saving frame: " + str(count))
            # Increase count
            count += 1
        except Exception as e:
            print("Error in image capture on frame {0}".format(count))
            print(e)
    num_frames_saved = len(os.listdir(save_dir))
    print("Total frames saved: " + str(num_frames_saved))
    print("Finished getting frames")
    # TODO: Fix this next line by checking that these numbers are correct - maybe print them out?
    if num_frames_saved == vidcap_metrics["num_frames_to_save"]:
        success = True
    else:
        success = False
    print(f"All frames successfully saved: {success}")
    if not success:
        raise


VideoToFramesOp = func_to_container_op(
    video_to_frames_func,
    base_image="europe-west1-docker.pkg.dev/hoodat-sandbox/hoodat-sandbox-kfp-components/video_to_frames",
    output_component_file="component.yaml",
)
