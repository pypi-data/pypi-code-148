import click


from tagbackup.lib import (
    api_post,
    download_file,
    file_exists,
    get_device_id,
    get_s3_resource,
    show_upgrade_available_message,
    tags_to_csv,
)


@click.command()
@click.argument("tags", nargs=-1)
@click.option(
    "--filename",
    help="Specify a local filename to write to (otherwise it will use the original upload filename)",
    default=None,
    type=click.Path(exists=False, dir_okay=False),
)
@click.option(
    "--overwrite", is_flag=True, help="Overwrite existing file (if it exists)"
)
def pull(tags, filename, overwrite):
    """
    Learn more at https://tagbackup.com/docs/client/pull
    """
    device_id = get_device_id()
    if not device_id:
        raise click.ClickException("this device is not linked to TagBackup")

    # bail out if no tags provided
    if len(tags) < 1:
        raise click.ClickException(
            "no tags provided. For more information visit https://tagbackup.com/docs/client/pull"
        )

    # bail out if we're about to overwrite an existing file
    if filename and not overwrite and file_exists(filename):
        raise click.ClickException(
            f"a file already exists called {filename}. You can overwrite this file using the --overwrite flag. Learn more at https://tagbackup.com/docs/client/pull"
        )

    # POST details to tagbackup
    click.echo("Contacting TagBackup...")
    response = api_post(
        "v1/pull",
        device_id,
        {
            "tags": tags_to_csv(list(set(tags))),
        },
        True,
    )

    # bail on error
    if not response["is_valid"]:
        raise click.ClickException(response["error"])

    # get s3 resource
    resource = get_s3_resource(response["access_key"], response["access_secret"])
    if resource is None:
        raise click.ClickException(
            "there was a problem communicating with your S3 bucket"
        )

    # use the original filename if none was passed in
    if filename is None:
        filename = response["orig_filename"]
        if not overwrite and file_exists(filename):
            raise click.ClickException(
                f"a file already exists called {filename}. You can overwrite this file using the --overwrite flag. Learn more at https://tagbackup.com/docs/client/pull"
            )

    # download file
    success = download_file(
        resource, filename, response["bucket"], response["filename"]
    )
    if not success:
        raise click.ClickException("there was a problem downloading to your S3 bucket")

    # success
    click.echo("Done!")
    show_upgrade_available_message(response)
