# coding=utf-8
import datetime
import json
import os
import pathlib
import time
from multiprocessing.pool import Pool
from time import sleep

import click
import humanize
from prettytable import PrettyTable

from rebotics_sdk.cli.common import shell, configure, roles, set_token
from .draw import draw_annotated_drawing
from .renderers import format_full_table
from .utils import ReboticsCLIContext, app_dir, pass_rebotics_context, read_saved_role, process_role, \
    downloads_with_threads, save_masks, get_segmentation, refresh_url, get_segmentation_mode
from ..advanced.flows import FileUploadError
from ..advanced.packers import ClassificationDatabasePacker, ClassificationDatabaseException, \
    DuplicateFeatureVectorsException
from ..providers import AdminProvider, RetailerProvider
from ..utils import uri_validator, get_filename_from_url

OPENCV_INSTALLED = True
try:
    import cv2
except ModuleNotFoundError:
    OPENCV_INSTALLED = False


@click.group()
@click.option('-f', '--format', default='table', type=click.Choice(['table', 'id', 'json']), help='Result rendering')
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode')
@click.option('-c', '--config', type=click.Path(), default='admin.json', help="Specify what config.json to use")
@click.option('-r', '--role', default=lambda: read_saved_role('admin'), help="Key to specify what admin to use")
@click.version_option()
@click.pass_context
def api(ctx, format, verbose, config, role):
    """
    Admin CLI tool to communicate with dataset API
    """
    process_role(ctx, role, 'admin')
    ctx.obj = ReboticsCLIContext(
        role,
        format,
        verbose,
        os.path.join(app_dir, config),
        provider_class=AdminProvider
    )


def get_retailer_version_task(retailer_dict):
    retailer_provider = RetailerProvider(host=retailer_dict['host'], retries=1, timeout=5)
    try:
        response = retailer_provider.version()
        version = response['version']
        uptime = humanize.naturaldelta(datetime.timedelta(seconds=int(response['uptime'])))
    except Exception:
        version = 'not working'
        uptime = '---'

    d = [
        retailer_dict['codename'],
        retailer_dict['title'],
        version,
        uptime,
        retailer_dict['host'],
    ]
    return d


@api.command()
@click.argument('title', type=click.STRING)
@click.argument('group', type=click.STRING)
@click.argument('description', type=click.STRING)
@click.argument('yaml_template', type=click.File())
@pass_rebotics_context
def save_test_case(ctx, title, group, description, yaml_template):
    """
    Save test case in core.
    ARGS:
        title - STR,
        group - STR,
        description - STR,
        yaml_template - File
    """
    click.echo('Save core test case')
    yaml_template = yaml_template.read()

    try:
        ctx.provider.create_core_test_case(title=title,
                                           group=group,
                                           description=description,
                                           yaml_template=yaml_template)
        click.echo('Done')
    except Exception as exc:
        raise click.ClickException(str(exc))


@api.command()
@click.argument('title', type=click.STRING)
@click.argument('group', type=click.STRING)
@click.argument('description', type=click.STRING)
@click.argument('yaml_template', type=click.File())
@click.option('--target', type=click.Path(exists=False, file_okay=True, dir_okay=True), default=None)
@pass_rebotics_context
def retrieve_test_case_data(ctx, title, group, description, yaml_template, target):
    """
    Retrieve data for test case from core.
    ARGS:
        title - STR,
        group - STR,
        description - STR,
        yaml_template - File,
        target - Path
    """
    click.echo('Rendering test_case data')
    yaml_template = yaml_template.read()

    try:
        res = ctx.provider.retrieve_core_test_case_data(title=title,
                                                        group=group,
                                                        description=description,
                                                        yaml_template=yaml_template)

        if target is None:
            ctx.format_result(res)
        else:
            target = pathlib.Path(target)
            if target.is_dir():
                target = target / f"test_case_{time.strftime('%d-%m-%Y_%H:%M')}.json"
            with open(target, 'w') as fd:
                fd.write(json.dumps(res, indent=2))
                click.echo(f'Download to {target}')
    except Exception as exc:
        raise click.ClickException(str(exc))


@api.command()
@click.argument('retailer')
@pass_rebotics_context
def configurations(ctx, retailer):
    """
        Fetch retailer configurations variables
    """
    try:
        res = ctx.provider.get_configurations(retailer)
        ctx.format_result(res)
    except Exception as exc:
        raise click.ClickException(str(exc))


@api.command()
@click.argument('retailer')
@pass_rebotics_context
def mobile_configurations(ctx, retailer):
    """
    Fetch configurations for mobile application for retailer
    """
    res = ctx.provider.get_mobile_configurations(retailer)
    ctx.format_result(res)


@api.command()
@click.option('-n', '--notify', is_flag=True)
@click.option('-d', '--delay', type=click.INT, default=60)
@pass_rebotics_context
def retailer_versions(ctx, notify, delay):
    """Fetch retailer versions and their meta information"""
    click.echo("For better experience use: \n"
               "https://versions.fyn.rocks/ and https://tracker.fyn.rocks/")

    if notify:
        if ctx.verbose:
            click.echo('Using notify option', err=True)

        try:
            from pynotifier import Notification
            Notification(
                title='Subscribed to the notifications',
                description='You will receive notifications for retailer updates',
            ).send()
        except ImportError:
            raise click.ClickException("You can't use notify function")

    provider = ctx.provider
    if ctx.verbose:
        click.echo('Fetching info from rebotics admin.', err=True)
    retailers = provider.get_retailer_list()
    prev_results = []
    results = []
    pool = Pool(len(retailers))

    while True:
        try:
            if ctx.verbose:
                click.echo('Fetching the retailer versions', err=True)
            results = pool.map(get_retailer_version_task, retailers)

            if not notify:
                break

            for prev_result in prev_results:
                retailer_codename = prev_result[0]
                previous_version = prev_result[2]
                for result in results:
                    if result[0] == retailer_codename:
                        current_version = result[2]
                        if previous_version != current_version:
                            notification_message = 'Retailer {} updated from version {} to {}'.format(
                                retailer_codename,
                                previous_version,
                                current_version
                            )
                            click.echo(notification_message)
                            Notification(
                                title=notification_message,
                                description='Current uptime is: {}'.format(result[3]),
                                duration=30,
                                urgency=Notification.URGENCY_CRITICAL,
                            ).send()
            del prev_results
            prev_results = results
            sleep(delay)
        except KeyboardInterrupt:
            break

    table = PrettyTable()
    table.field_names = ['codename', 'title', 'version', 'uptime', 'host']
    for result in results:
        table.add_row(result)
    click.echo(table)


@api.command()
@click.argument('retailer')
@click.option('--v2', is_flag=True, show_default=True, default=False, help="Use models v2 API")
@pass_rebotics_context
def models(ctx, retailer, v2):
    """
        Fetch and display retailer NN configurations
    """
    try:
        if v2:
            ctx.format_result(
                ctx.provider.get_models_conf_v2(codename=retailer)
            )
        else:
            ctx.format_result(
                ctx.provider.get_retailer_tf_models(codename=retailer)
            )
    except Exception as exc:
        raise click.ClickException(str(exc))


@api.command()
@click.argument('retailer', type=click.STRING)
@click.argument('url', type=click.STRING)
@pass_rebotics_context
def set_retailer_url(ctx, retailer, url):
    try:
        ctx.provider.update_host(retailer, url)
    except Exception as exc:
        raise click.ClickException(str(exc))
    else:
        click.echo('Set new host for retailer %s' % retailer)


@api.command()
@click.option('-r', '--retailer', help="Retailer codename", prompt=True)
@click.option('-m', '--model', help="Model codename", prompt=True)
@click.option('-i', '--images', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('-l', '--labels', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('-f', '--features', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('-c', '--check-duplicates', is_flag=True, help="MD5 checker simple")
@pass_rebotics_context
def pack_and_import_classification_db(ctx, retailer, model, images, labels, features, check_duplicates):
    """Pack classification database to single .rcdb file and import it to the Rebotics Admin

\b
db/
├── custom_folder
│   ├── image_2.png
│   └── image_1.png
├── features.txt
└── labels.txt

    It is a single step command with equivalent of running two commands:

admin pack-classification-db --features features.txt --labels labels.txt --images ./custom_folder/ --target classification.rcdb

admin import_classification_db --retailer delta --model test_code classification.rcdb
    """
    ext = ClassificationDatabasePacker.extension
    with ctx.provider.rcdb.import_flow(retailer, model, ext) as flow:
        if ctx.verbose:
            click.echo("Creating import request: \n"
                       "retailer: {}\n"
                       "model: {}\n"
                       "extension: {}".format(retailer, model, ClassificationDatabasePacker))

        packer = ClassificationDatabasePacker(destination=None, progress_bar=True, check_duplicates=check_duplicates)
        if ctx.verbose:
            click.echo("Packing from provided values: \n"
                       "labels: {labels} \n"
                       "features: {features} \n"
                       "images: {images}".format(labels=labels, features=features, images=images))

        try:
            packed = packer.pack(labels, features, images)
            packed.seek(0)
        except DuplicateFeatureVectorsException as exc:
            handle_duplicates(ctx, exc.duplicates)
            raise click.ClickException(str(exc))
        except ClassificationDatabaseException as exc:
            raise click.ClickException(str(exc))

        if ctx.verbose:
            click.echo("Import request: {}".format(flow.import_request))

        try:
            flow.upload_file(packed, progress_bar=True)
        except FileUploadError as exc:
            click.echo(str(exc))
            raise

        click.echo("Import completed. Reference database id: {}".format(flow.import_request['id']))


@api.command()
@click.option('-r', '--retailer', help="Retailer codename", prompt=True)
@click.option('-m', '--model', help="Model codename", prompt=True)
@click.argument('filepath', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@pass_rebotics_context
def import_classification_db(ctx, retailer, model, filepath):
    """Import rcdb file to Rebotics Admin. Example usage:

    admin import_classification_db --retailer delta --model test_code classification.rcdb

    """
    extension = os.path.split(filepath)[-1].split('.')[-1]
    if ctx.verbose:
        click.echo("Creating import request: \n"
                   "retailer: {}\n"
                   "model: {}\n"
                   "extension: {}".format(retailer, model, extension))

    with ctx.provider.rcdb.import_flow(retailer, model, extension) as flow:
        if ctx.verbose:
            click.echo("Import request: {}".format(flow.import_request))
        with open(filepath, 'rb') as packed:
            flow.upload_file(packed, progress_bar=True)

    click.echo("Import completed. Reference database id: {}".format(flow.import_request['id']))


def handle_duplicates(ctx, duplicates):
    unpacked = [
        [
            {
                'id': entry.index,
                'label': entry.label,
                'filename': entry.filename
            }
            for entry in group
        ] for group in duplicates
    ]
    if ctx.format == 'json':
        click.echo(json.dumps(unpacked, indent=2))
    elif ctx.format == 'table':
        for group in unpacked:
            format_full_table(group)
    elif ctx.format == 'id':
        click.echo("Duplicate id. New line separated for group; space separated inside of the group:")
        for group in duplicates:
            click.echo(" ".join([str(entry.index) for entry in group]))
    else:
        for group in duplicates:
            for entry in group:
                click.echo("{entry.index} {entry.label} {entry.filename}".format(entry=entry))
            click.echo('=' * 100)


@api.command()
@click.option('-i', '--images', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('-l', '--labels', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('-f', '--features', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('-c', '--check-duplicates', is_flag=True, help="MD5 checker simple")
@click.argument('target', type=click.Path(exists=False, file_okay=True, dir_okay=True), default='.')
@pass_rebotics_context
def pack_classification_db(ctx, images, labels, features, target, check_duplicates):
    """Pack classification database to single .rcdb file

\b
db/
├── custom_folder
│   ├── image_2.png
│   └── image_1.png
├── features.txt
└── labels.txt

    Example usage:
        admin pack-classification-db --features features.txt --labels labels.txt --images ./custom_folder/ --target classification.rcdb

    """
    target = pathlib.Path(target)
    if target.is_dir():
        target = target / "classification_db{}.{}".format(
            datetime.datetime.now().strftime('%Y-%m-%dZ%H%M'),
            ClassificationDatabasePacker.extension
        )
    packer = ClassificationDatabasePacker(
        destination=target,
        progress_bar=True,
        check_duplicates=check_duplicates
    )
    if ctx.verbose:
        click.echo("Packing from provided values: \n"
                   "labels: {labels} \n"
                   "features: {features} \n"
                   "images: {images}".format(labels=labels, features=features, images=images))
    try:
        packed = packer.pack(labels, features, images)
    except DuplicateFeatureVectorsException as exc:
        handle_duplicates(ctx, exc.duplicates)
        raise click.ClickException(str(exc))
    except ClassificationDatabaseException as exc:
        raise click.ClickException(str(exc))
    click.echo('Written to {}'.format(packed))


@api.group(name='rcdb')
def rcdb_group():
    click.echo("RCDB in rebotics admin is deprecated and will be removed in version 0.13.0")


@rcdb_group.command(name="previews-fs")
@click.argument("argument", type=click.STRING)
@click.option('-o', "--output", type=click.Path(exists=True, dir_okay=True, file_okay=False), default=".")
@click.option('-c', '--concurrency', default=8, type=click.INT)
@pass_rebotics_context
def rcdb_previews_fs(ctx, argument, output, concurrency):
    """
    Prepare previews file structure by the id, filepath or file url of the JSON formatted backup
    Make sure that extension is a valid JSON and extension in the admin is set like that
    """
    click.echo("Use `fvm rcdb unpack` command instead")


@api.group()
def stitching():
    pass


@stitching.command(name='setup')
@click.argument("argument", type=click.STRING)
@click.option('-o', "--output", type=click.Path(dir_okay=True, file_okay=False))
@click.option('-c', '--concurrency', default=8, type=click.INT)
@click.option('-d', '--draw', is_flag=True, help='To draw annotated frames')
@pass_rebotics_context
def stitching_setup(ctx, argument, concurrency, output, draw):
    """
    argument - id of stitching debug data from admin, or json file
    """
    if draw and not OPENCV_INSTALLED:
        raise click.ClickException(' OpenCv not found, but can be installed with: pip install opencv-python ')

    if output:
        output = pathlib.Path(output).absolute()
    else:
        output = pathlib.Path('.').absolute()

    output = output / f"stitching_{argument.replace(' ', '_')}"
    output.mkdir(parents=True, exist_ok=True)
    ctx.verbose_log(f"Target directory is: {output}")
    filepath = output / "definition.json"

    if argument.isdigit():
        backup_id = int(argument)
        callback_data = ctx.provider.get_core_callback_data(backup_id)
        definition = callback_data['data']

        ctx.verbose_log("Saving definition locally")
        with open(filepath, 'w') as fp:
            json.dump(definition, fp)

    elif uri_validator(argument):
        # argument is a url
        raise click.ClickException("not supported")
    else:
        ctx.verbose_log("Assuming we have a filepath")
        filepath = argument
        try:
            with open(filepath, 'rb') as fp:
                definition = json.load(fp)
        except Exception:
            raise click.ClickException(f"File is not supported. Please check it at {filepath}")

    if 'data' in definition:
        definition = definition['data']

    if ctx.verbose:
        ctx.format_result(definition['context'], force_format='json')

    files_to_load = []  # pair of remote_url to local path

    segmentation_filepath = output / "image_segmentation_debug.json"
    segmentation_url = definition.get("image_segmentation_debug", None)
    if segmentation_url is not None:
        files_to_load.append([segmentation_url, segmentation_filepath])
    else:
        draw = False
        ctx.verbose_log("Cannot draw bboxes, no image segmentation debug file is available")

    meta_df_filepath = output / "task_meta_df.csv"
    meta_df_url = definition.get("task_meta_df", None)
    if meta_df_url is not None:
        files_to_load.append([meta_df_url, meta_df_filepath])

    for call_count, call_data in enumerate(definition['calls']):
        call_folder = output / f"call_{call_count}"
        call_folder.mkdir(parents=True, exist_ok=True)

        input_data = call_data['input']

        stitching_input = {
            **input_data,
            'frame_paths': [],
            'output_file': str(call_folder),
            'result_image': str(call_folder / "local_stitching.jpeg"),
        }

        del stitching_input['frame_urls']
        # for backward compatible
        if 'annotated_frames' in stitching_input:
            del stitching_input['annotated_frames']

        # add stitching result image
        try:
            files_to_load.append([
                call_data['image_url'], call_folder / "server_stitched_image.jpeg"
            ])
        except Exception:
            ctx.verbose_log("No stitching image is available")

        if input_data.get('mask_od_url'):
            mask_od_path = call_folder / "mask_od.json"
            stitching_input['mask_od'] = str(mask_od_path)
            files_to_load.append([
                input_data['mask_od_url'], mask_od_path
            ])

        # register input files
        frames_folder = call_folder / "frames"
        frames_folder.mkdir(parents=True, exist_ok=True)

        for frame_url in input_data['frame_urls']:
            frame_path = frames_folder / get_filename_from_url(frame_url)
            stitching_input['frame_paths'].append(str(frame_path))
            files_to_load.append([
                frame_url, frame_path
            ])

        frames_folder = call_folder / "annotated_frames"
        frames_folder.mkdir(parents=True, exist_ok=True)

        annotated_frames = input_data.get('annotated_frames', [])
        if annotated_frames:
            for frame_url in annotated_frames:
                frame_path = frames_folder / get_filename_from_url(frame_url)
                files_to_load.append([
                    frame_url, frame_path
                ])

        ctx.verbose_log(f'Creating a stitching input for run #{call_count} into {call_folder}')
        with open(str(call_folder / "stitching_input.json"), 'w') as fp:
            json.dump(stitching_input, fp)

    ctx.verbose_log(f"Registered files for downloading: {len(files_to_load)}")

    downloads_with_threads(files_to_load, concurrency=len(files_to_load))
    click.echo(f"Stitching setup complete in: {output}")

    if draw:
        segmentation_per_image = get_segmentation(segmentation_filepath)
        mode = get_segmentation_mode(segmentation_per_image)
        if mode == 'remote_url':
            refreshed_urls = refresh_url(ctx.provider.refresh_url, segmentation_per_image)
            # save masks in output/all_masks
            save_masks(output, refreshed_urls)

        draw_annotated_drawing(
            root_folder=output,
            segmentation_per_image=segmentation_per_image,
            mode=mode,
            concurrency=concurrency
        )


api.add_command(shell, 'shell')
api.add_command(roles, 'roles')
api.add_command(configure, 'configure')
api.add_command(set_token, 'set_token')
