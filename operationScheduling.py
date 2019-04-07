from django.shortcuts import render
from operations.MRP import generateProduceOrder

'''
    生產排程
    FCFS
    input: productionOrder 生產訂單
'''
def scheduling(time, car):
    productionOrder = generateProduceOrder(time, car)
    productionOrder = sorted(productionOrder, key = lambda x : x[2])
    productionOrder = productionOrder[0]
    totalTime = 0  # 總完工時間
    totalDueTime = 0  # 總延遲時間
    avgFlowTime = 0  # 平均流程時間
    avgLateness = 0  # 平均延遲時間
    avgJob = 0  # 平均工作數
    job = []
    processingTime = []  # 處理時間
    flowtime = []  # 流程時間
    dueTime = []  # 到期時間
    lateness = []  # 延遲時間
    for order in productionOrder:
        #for orderdetail in order:
        job.append(order[0])

        processingTime.append(float(order[1]))
        dueTime.append(order[3])
        flowtime.append(sum(processingTime))
        lateness.append(0 if (sum(flowtime) - order[3]) <= 0
                        else (sum(flowtime) - order[3]))

    avgFlowTime = round(sum(flowtime) / len(job), 2)
    avgLateness = round(sum(lateness) / len(job), 2)
    totalTime = sum(processingTime)
    avgJob = round(sum(flowtime) / sum(processingTime), 2)

    ### result ###
    table = "工作順序\t處理時間\t流程時間\t 到期日\t延遲天數\n" + \
            "--------------------------------------------------\n"
    for i in range(0, len(job)):
        table += "{:4}\t{:4}\t{:4}\t{:4}\t{:4}\n".format(job[i], processingTime[i], flowtime[i], dueTime[i], lateness[i])

    efficiency = "平均流程時間\t%d\n" % avgFlowTime + \
                 "平均延遲時間\t%f\n" % avgLateness + \
                 "總完工時間為\t%d\t，工作中心的平均工作數\t%f" % (totalTime, avgJob)
    return table, efficiency
