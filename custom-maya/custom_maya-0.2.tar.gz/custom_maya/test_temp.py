# import asyncio
#
# async def count(file_name='name'):
#     print(f'{file_name}获取文件路径')
#     print(f'{file_name}获取文件对象')
#     print(f'{file_name}开始文件内容读取和处理...')
#     await asyncio.sleep(1)
#     print(f'{file_name}文件处理完成。将数据写入本地文件...')
#     await asyncio.sleep(0.5)
#     print(f'{file_name}文件读写完成。')
#
# async def main():
#     l = [count(file_name=f'file_name_{i}') for i in range(10)]
#
#     await asyncio.gather(l)
#
# asyncio.run(main())