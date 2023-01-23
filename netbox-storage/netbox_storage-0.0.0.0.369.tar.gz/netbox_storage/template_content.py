from extras.plugins import PluginTemplateExtension
from itertools import chain
import logging

from netbox_storage.models import Drive, Partition, PhysicalVolume, LogicalVolume


class RelatedDrives(PluginTemplateExtension):
    model = "virtualization.virtualmachine"

    def full_width_page(self):
        obj = self.context.get("object")

        drives = Drive.objects.filter(
            virtual_machine=obj
        )
        # drive_table = RelatedDriveTable(
        #     data=drives
        # )
        # volumes = LinuxVolume.objects.all()
        # exclude_drive_id = []
        # for inc in volumes.all():
        #     for drive in inc.drives.all():
        #         exclude_drive_id.append(drive.id)
        # unmapped_drives = Drive.objects.filter(
        #     virtual_machine=obj
        # ).exclude(id__in=exclude_drive_id).order_by('identifier')

        # all_volumes = LinuxVolume.objects.all()
        # display_volume = []
        # for inc in all_volumes:
        #     display_volume = inc.drives.all().intersection(drives)
        partitions = []
        for drive in drives:
            partitions = Partition.objects.filter(
                drive=drive
            )

        physical_volumes = PhysicalVolume.objects.filter(
            partition__in=partitions
        )

        volume_group_list = physical_volumes.values_list('vg', flat=True)

        logical_volumes = LogicalVolume.objects.filter(
            vg__in=volume_group_list
        )

        result_list = list(chain(drives, partitions, volume_group_list, logical_volumes))
        logger = logging.getLogger('netbox.plugins.netbox_storage')
        logger.warning(f'{result_list}')

        platform = obj.platform
        if platform is not None:
            if platform.name.lower().__contains__('windows'):
                return self.render(
                    "netbox_storage/inc/windowsvolume_box.html",
                    extra_context={
                        # "volumes": volumes,
                        # "unmapped_drives": unmapped_drives,
                        "type": type(obj.platform),
                        # "display_volume": display_volume
                        "physical_volumes": physical_volumes
                    },
                )
            elif platform.name.lower().__contains__('linux'):
                return self.render(
                    "netbox_storage/inc/linuxvolume_box.html",
                    extra_context={
                        "partitions": partitions,
                        "physical_volumes": physical_volumes,
                        "logical_volumes": logical_volumes
                    },
                )
        else:
            return self.render(
                "netbox_storage/inc/unknown_os_box.html",
            )


template_extensions = [RelatedDrives]
