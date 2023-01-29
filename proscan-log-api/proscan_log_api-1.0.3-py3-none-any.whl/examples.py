# from datetime import datetime

# from proscan_log_api.tcs_log_api import SlowControlClient, TcsTraceClient

# # if __name__ == "__main__":
# #     file_path_slow = "./tests/slow_control_test_data.txt"
# # file_path_tcs = "/mnt/TCSlogs/G2/TcsTrace/pg2tds.20221202-080420.trcTds"
# # api = SlowControl("./")
# # metadata = api.metadata(file_path=file_path_slow)
# # if not metadata.empty:
# #     print(metadata.to_dict())
# # api = SlowControl()
# # data = api.get(
# #     start_datetime=datetime(year=2022, month=11, day=30),
# #     end_datetime=datetime(
# #         year=2022,
# #         month=12,
# #         day=2,
# #     ),
# #     area="G2",
# # )
# # if not data.empty:
# #     print(data.to_dict())
# # parse_tcs_trace(file_path=file_path_tcs)
# # print(
# #     get_tcs_files(
# #         root_dir="/mnt/TCSlogs/",
# #         area="G2",
# #         tcs_type="slow",
# #         start_datetime=datetime(
# #             year=2022, month=11, day=30, hour=6, minute=45, second=26, microsecond=0
# #         ),
# #     )
# # )
# import pandas as pd

# slow_logs = SlowControlClient(root_dir="/mnt/tcs_logs/")
# logs = slow_logs.get(
#     system="tvs",
#     folders="g2prod/production/VxWorks/Log/,g3prod/production/VxWorks/Log/,o2prod/production/VxWorks/Log/",
#     start_datetime=datetime(year=2022, month=11, day=30),
#     end_datetime=datetime(year=2022, month=12, day=1),
#     area="G2",
# )
# print(logs)

# print(logs.data[logs.data.index.duplicated()].sort_values("timestamp"))

# print("\n\n")
# duplicat = logs.data.loc[datetime.fromisoformat("2022-11-30 20:19:29")]
# # print(pd.DataFrame(result))
# duplicat.to_csv("test.csv")
# trace_logs = TcsTraceClient(root_dir="/mnt/tcs_logs/")
# logs = trace_logs.get(
#     system="tds",
#     folders="g2prod/production/VxWorks/Log/,g3prod/production/VxWorks/Log/,o2prod/production/VxWorks/Log/",
#     start_datetime=datetime(
#         year=2022,
#         month=12,
#         day=1,
#         hour=10,
#     ),
#     end_datetime=datetime(
#         year=2022,
#         month=12,
#         day=1,
#         hour=11,
#     ),
#     area="G2",
# )

# print(logs)
# from .pass_log_api import PassClient
# from datetime import datetime
# from time import time

# PASS_LOG_DATA_DIR_ROOT = "/mnt/proscan-fs/"
# PASS_LOG_DATA_FOLDERS = "PG2TC1-VME-PASS,PG2TC2-VME-PASS,PG3TC1-VME-PASS,PG3TC2-VME-PASS,PMPTC1-VME-PASS,PMPTC2-VME-PASS,PO2TC1-VME-PASS,PO2TC2-VME-PASS"
# if __name__ == "__main__":
#     start = time()
#     api = PassClient(root_dir=PASS_LOG_DATA_DIR_ROOT, folders=PASS_LOG_DATA_FOLDERS)
#     _ = api.get(
#         area="G2",
#         start_datetime=datetime(year=2022, month=1, day=4),
#         end_datetime=datetime(year=2022, month=1, day=5),
#         override_limit=True,
#     )
#     # _ = api.get(
#     #     area="G2",
#     #     start_datetime=datetime(year=2022, month=4, day=1),
#     #     end_datetime=datetime(year=2022, month=7, day=31),
#     #     override_limit=True,
#     # )
#     # _ = api.get(
#     #     area="G2",
#     #     start_datetime=datetime(year=2022, month=8, day=1),
#     #     end_datetime=datetime(year=2022, month=11, day=30),
#     #     override_limit=True,
#     # )
#     print("Execution Time: ", time() - start)
