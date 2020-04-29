import psutil

cpus = psutil.cpu_times()
print("CPU的详细信息:{}".format(cpus))

# psutil获取系统cpu使用率的方法是cpu_percent()
# 两个参数，分别是interval和percpu,
# interval指定的是计算cpu使用率的时间间隔，
# percpu则指定是选择总的使用率还是每个cpu的使用率。(默认为False)
percent = psutil.cpu_percent(interval=5)
print(f"当前CPU总使用率为:{percent}%")

percent = psutil.cpu_percent(interval=1, percpu=True)
print(f"当前每个CPU使用率为:{percent}")

# cpu详细使用率
times_percent = psutil.cpu_times_percent(interval=1, percpu=False)
print(f"当前CPU总详细使用率为:{times_percent}%")


# cpu核数
logical_count = psutil.cpu_count()
print(f"CPU逻辑核数:{logical_count}")

cpu_count = psutil.cpu_count(logical=False)
print(f"CPU物理核数:{logical_count}")


# cpu状态
stats = psutil.cpu_stats()
print(f"cpu当前状态:{stats}")

# cpu频率
freq = psutil.cpu_freq()
print(f"cpu的频率:{freq}")

#这里是内存部分
mem=psutil.virtual_memory()
print('获取内存完整信息：', mem)
print('获取内存总数：', mem.total/(1024*1024*1024),'G')
print('获取内存空闲总数：', mem.free/(1024*1024*1024),'G')
print('获取swap分区的内存信息：', psutil.swap_memory())