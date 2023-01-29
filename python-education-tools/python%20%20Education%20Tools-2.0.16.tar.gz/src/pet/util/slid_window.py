def slid_window(s, size=2,strid=1):
    ns=[s[i:i+size] for i in s[:-size+1:strid]]
    return ns

print(slid_window(tuple(range(1,5)), 2,1))

data=range(1,5)
print(f'原始数据集{list(data)}')
window_size=2
stride=1 #跳跃元素个数，1为依次滑动
slid_data=[sum(data[i:i+window_size]) for i,_ in enumerate(data[:-window_size+1:stride])]
print(f'得到新数据集{slid_data}')
