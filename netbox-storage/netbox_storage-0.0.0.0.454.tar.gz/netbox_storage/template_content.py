from extras.plugins import PluginTemplateExtension
from itertools import chain
import logging

from netbox_storage.models import Drive, Partition, PhysicalVolume, LogicalVolume, VolumeGroup, LinuxVolume


class LVMModel:
    def __init__(self, lv_name, path, fs, size, vg_name, pv_list=None, partition_list=None, drive_list=None):
        self.lv_name = lv_name
        self.path = path
        self.fs = fs
        self.size = size
        self.vg_name = vg_name
        self.pv_list = pv_list
        self.partition_list = partition_list
        self.drive_list = drive_list


class RelatedDrives(PluginTemplateExtension):
    model = "virtualization.virtualmachine"

    def full_width_page(self):
        obj = self.context.get("object")

        # --- Try via Logical Volume
        logicalvolumes = LogicalVolume.objects.all()
        lvm_list = []
        logger = logging.getLogger('netbox.plugins.netbox_storage')

        # appending instances to list
        for lv in logicalvolumes:
            logger.warning(f'{lv.vg}')
            lvm_list.append(LVMModel(lv.lv_name, lv.path, lv.fs, lv.size, lv.vg.vg_name))
            physical_volumes = PhysicalVolume.objects.all()
            physical_volume_list = []
            partition_list = []
            logger.warning(f'vor for {physical_volumes}')
            for physical_volume in physical_volumes:
                logger.warning(f'nach for {physical_volume}')
                if physical_volume.vg == lv.vg:
                    physical_volume_list.append(physical_volume)
                    lvm_model = lvm_list[-1]
                    lvm_model.pv_list = physical_volume_list
                    partition_list.append(physical_volume.partition)
                    lvm_model.partition_list = partition_list
            #         partitions = Partition.objects.all()
            #         partition_list = []
            #         for partition in partitions:
            #             if partition.device == physical_volume.pv_name:
            #                 partition_list.append(f"{partition.device}-{partition.size}")
            #                 lvm_model.partition_list = partition_list

        logger.warning(f'{lvm_list}')
        linux_volume_list = []
        linuxvolumes = LinuxVolume.objects.all()
        linux_volume_list = list(LinuxVolume.objects.all())
        logger.warning(f'linuxvolumes for {linux_volume_list}')

        # drives = Drive.objects.filter(
        #     virtual_machine=obj
        # )
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


        #partitions = []
        #for drive in drives:
        #    partitions = Partition.objects.filter(
        #        drive=drive
        #    )

        # hd_partition_list = []
        # for drive in drives:
        #     hd_partition = [drive]
        #     partitions = Partition.objects.filter(
        #         drive=drive
        #     ).values_list()
        #     hd_partition.append(partitions)
        #     hd_partition_list.append(hd_partition)

        #physical_volumes = PhysicalVolume.objects.filter(
        #    partition__in=partitions
        #)

        #volume_group_list = physical_volumes.values_list('vg', flat=True)

        #logical_volumes = LogicalVolume.objects.filter(
        #    vg__in=volume_group_list
        #)

        # result_list = list(chain(drives, partitions, volume_group_list, logical_volumes))
        # logger.warning(f'{result_list}')


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
                        #"physical_volumes": physical_volumes
                    },
                )
            elif platform.name.lower().__contains__('linux'):
                return self.render(
                    "netbox_storage/inc/linuxvolume_box.html",
                    extra_context={
                        "lvm_list": lvm_list,
                        "linux_volume_list": linux_volume_list,
                        #"physical_volumes": physical_volumes,
                        #"logical_volumes": logical_volumes,
                        #"hd_partition_list": hd_partition_list
                    },
                )
        else:
            return self.render(
                "netbox_storage/inc/unknown_os_box.html",
            )


template_extensions = [RelatedDrives]
