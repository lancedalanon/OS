"""CPU Scheduling Simulator

COMP 20103 Operating Systems Project for the 1st Semester 2021-2022
by Dalanon, Lance Orville R. BSIT 2-2

The project's objective is to simulate one, as selected, of the four (4)
of the CPU scheduling policies which are (FCFS - First Come First Serve,
SJF - Shortest Job First, SRTF - Shortest Remaining Time First,
and RR - Round Robin).

The user inputs data for the simulator to calculate the following:
Average Response Time, Average Turnaround Time, Average Waiting Time,
and Overall CPU Usage. It also generates a Gantt Chart. The maximum
queue allowed for this simulator is limited up to only five (5) processes.

To avoid errors, the program is set to take IDs from user input to only 1-5.
Zeroes and negatives are not allowed for IDs because the zeroes get replaced
with 'I's representing "Idle Time", furthermore, negative inputs to Arrival and
Burst Times are not allowed as that would mean the system is unstable in OS.

No modules are needed to import for running this program.
"""
class FCFS:
    """Calculates Average Response Time, Average Turnaround Time,
    Average Waiting Time, Overall CPU Usage, and generates
    Gantt Chart using FCFS CPU Scheduling Algorithm.

    First Come First Served (FCFS) is an OS process scheduling
    algorithm that automatically executes queued requests and
    processes by the order of their arrival time.
    """
    def sortingData(self, data_processed):
        """Sorts and gets both response and completion times to a list.

        Data from schedule_data get processed into data_processed.
        Data is modified into removing the last two items of the list
        (0, burst_time) as it is unnecessary for the FCFS algorithm.
        We then get the sorted IDs as well as response and
        completion time into the list through iteration separately.
        Data are then transferred to other functions within this class
        for them to calculate and make a Gantt Chart.

        Parameters:
            data_processed (list): Data transferred from schedule_data.

        Returns:
            None
        """
        data_processed.sort(key=lambda x: x[1])
        modified_data = [i[:-2] for i in data_processed]
        """
        Sorts according to the Arrival Time and removes 0 and excess burst_time.
        """
        temp_id = data_processed.copy()
        process_id = [i[0] for i in temp_id]
        """
        Transfers all sorted IDs into a list copy for the Gantt Chart.
        """
        response_time = []
        completion_time = []
        start_value = 0

        for i in range(len(modified_data)):
            if start_value < modified_data[i][1]:
                start_value = modified_data[i][1]
            response_time.append(start_value)
            start_value = start_value + modified_data[i][2]
            end_value = start_value
            completion_time.append(end_value)
            modified_data[i].append(end_value)

        RT = FCFS.calculateResponseTime(self, response_time)
        TT = FCFS.calculateTurnaroundTime(self, modified_data)
        WT = FCFS.calculateWaitingTime(self, modified_data)
        idle_time_line, final_bot_line = FCFS.ganttChart(self, response_time, completion_time)
        CPU = FCFS.calculateUsage(self, completion_time, process_id, idle_time_line)
        FCFS.printAllData(self, process_id, modified_data, response_time, completion_time)
        FCFS.printGanttChart(self, process_id, response_time, idle_time_line, final_bot_line)
        FCFS.calcutationData(self, RT, TT, WT, CPU)

    def calculateResponseTime(self, response_time):
        """Calculates average response time.

        Parameters:
            response_time (list): Data of response times.

        Returns:
            float: Calculated average of response times.
        """
        average_response_time = sum(response_time) / len(response_time)
        return average_response_time

    def calculateTurnaroundTime(self, modified_data):
        """Calculates Average Turnaround Time.

        Parameters:
            modified_data (list): Data modified from sortingData.

        Returns:
            float: Calculated average turnaround time.
        """
        total_turnaround_time = 0
        for i in range(len(modified_data)):
            turnaroundTime = modified_data[i][3] - modified_data[i][1]
            """
            Turnaround Time = Completion Time - Arrival Time
            """
            total_turnaround_time = total_turnaround_time + turnaroundTime
            modified_data[i].append(turnaroundTime)
        average_turnaround_time = total_turnaround_time / len(modified_data)
        return average_turnaround_time

    def calculateWaitingTime(self, modified_data):
        """Calculates Average Waiting Time.

        Parameters:
            modified_data (list): Data modified from sortingData.

        Returns:
            float: Calculated average waiting time.
    `   """
        total_waiting_time = 0
        for i in range(len(modified_data)):
            waitingTime = modified_data[i][4] - modified_data[i][2]
            """
            Waiting Time = Turnaround Time - Burst Time
            """
            total_waiting_time = total_waiting_time + waitingTime
            modified_data[i].append(waitingTime)
        average_waiting_time = total_waiting_time / len(modified_data)
        return average_waiting_time

    def printAllData(self, process_id, modified_data, response_time, completion_time):
        """Prints Out All Of The Data To Be Calculated.

        Prints Processor IDs, Arrival Time, Burst Time, Start Time, and End Time
        In a Gantt Chart form.

        Parameters:
            process_id (list): Data of processor IDs.

            modified_data (list): Data modified from sortingData.

            response_time (list): Data of response times.

            completion_time (list): Data of completion times.

        Returns:
            None
        """
        id_processed = [i[0] for i in modified_data]
        arrival_time = [i[1] for i in modified_data]
        burst_time = [i[2] for i in modified_data]
        response_time = response_time[:-1]

        # Prints all IDS in Gantt Chart form
        print("\nProcess_Name:")
        for i in range(len(process_id)):
            print("+-----", end="--")
        print("+")

        mid_line = ['\tP{0}\t|'.format(elem) for elem in process_id]
        print("|", ''.join(mid_line))

        for i in range(len(process_id)):
            print("+-----", end="--")
        print("+")
        print("\t", '\t\t'.join(str(p) for p in process_id))

        # Prints all Arrival Times in Gantt Chart form
        print("\nArrival_Time:")
        for i in range(len(arrival_time)):
            print("+-----", end="--")
        print("+")

        mid_line = ['\t{0}\t|'.format(elem) for elem in arrival_time]
        print("|", ''.join(mid_line))

        for i in range(len(arrival_time)):
            print("+-----", end="--")
        print("+")
        print("\t", '\t\t'.join(str(p) for p in process_id))

        # Prints all Burst Times in Gantt Chart form
        print("\nBurst_Time:")
        for i in range(len(burst_time)):
            print("+-----", end="--")
        print("+")

        mid_line = ['\t{0}\t|'.format(elem) for elem in burst_time]
        print("|", ''.join(mid_line))

        for i in range(len(burst_time)):
            print("+-----", end="--")
        print("+")
        print("\t", '\t\t'.join(str(p) for p in process_id))

        # Prints all Start Times in Gantt Chart form
        print("\nStart_Time:")
        for i in range(len(response_time)):
            print("+-----", end="--")
        print("+")

        mid_line = ['\t{0}\t|'.format(elem) for elem in response_time]
        print("|", ''.join(mid_line))

        for i in range(len(response_time)):
            print("+-----", end="--")
        print("+")
        print("\t", '\t\t'.join(str(p) for p in id_processed))

        # Prints all End Times in Gantt Chart form
        print("\nEnd_Time:")
        for i in range(len(completion_time)):
            print("+-----", end="--")
        print("+")

        mid_line = ['\t{0}\t|'.format(elem) for elem in completion_time]
        print("|", ''.join(mid_line))

        for i in range(len(completion_time)):
            print("+-----", end="--")
        print("+")
        print("\t", '\t\t'.join(str(p) for p in id_processed))

    def ganttChart(self, response_time, completion_time):
        """Part One of the Gantt Chart Generation

        Gantt Chart is generated by firstly determining here whether
        the first value of the response time starts with a zero
        or numbers more than that, if the former, it will start
        by iterating through giving out an idle time line to be
        subtracted from both response and completion time.
        The resulting value is then concatenated to the list
        and forms a new response time and removes duplicates
        through final iteration and becomes the bottom line for
        the later Gantt Chart. If the latter however, the same
        method is applied except after inserting the zero at the
        start it will get the idle time which is then extended to
        the idle time line and the rest follows the same with the
        former.

        Parameters:
            response_time (list): Data of response times.

            completion_time (list): Data of completion times.

        Returns:
            idle_time_line (list): Data of idle times.

            final_bot_line (list): Data for the bottom part
                                   of the Gantt Chart
        """
        first_response_value = response_time[0:1]
        idle_time_line = []
        final_bot_line = []

        for i in range(len(first_response_value)):
            i = int(first_response_value[i])

            if i == 0:

                final_complete_value = completion_time[-1:]
                response_time.extend(final_complete_value)
                idle_time_line = [a - b for a, b in zip(response_time[1:], completion_time[0:])]
                idle_time_line.insert(0, 0)
                temp_response_time = [x - y for x, y in zip(response_time, idle_time_line)]
                new_response_time = temp_response_time + response_time
                for i in new_response_time:
                    if i not in final_bot_line:
                        final_bot_line.append(i)
                final_bot_line.sort()

            elif i != 0:

                final_complete_value = completion_time[-1:]
                response_time.extend(final_complete_value)
                response_time.insert(0, 0)
                x = response_time[:-5]
                y = response_time[1:-5]
                new_response_time = [y - x for x, y in zip(x, y)]
                idle_time_line.extend(new_response_time)
                idle_time = [a - b for a, b in zip(response_time[2:], completion_time[0:])]
                idle_time_line.extend(idle_time)
                final_bot = [a - b for a, b in zip(response_time[1:], idle_time_line)]
                response_time.extend(final_bot)
                for i in response_time:
                    if i not in final_bot_line:
                        final_bot_line.append(i)
                final_bot_line.sort()

        return idle_time_line, final_bot_line

    def printGanttChart(self, process_id, response_time, idle_time_line, final_bot_line):
        """Part Two of the Gantt Chart Generation

        Continues synthesis and prints out the Gantt Chart
        according to the synthesized data.

        The first if-elif statement turns all of the zeroes in the
        list into 'I's which stands for "Idle".

        The second section of this function is where the Gantt Chart is
        generated.

        Parameters:
            process_id (list): Data of processor IDs.

            response_time (list): Data of response times.

            idle_time_line (list): Data of idle times.

            final_bot_line (list): Data for the bottom part of the Gantt Chart

        Returns:
            None
        """
        first_response_value = response_time[0:1]
        b = process_id
        c = []

        if first_response_value == 0:

            idle_time_line.insert(0, 0)
            a = ['I' if int(el) > 0 else 0 for el in idle_time_line]
            result = [None] * (len(a) + len(b))
            result[::1] = a
            result[0::1] = b
            c = [i for i in result if i != 0]

        elif first_response_value != 0:

            a = ['I' if int(el) > 0 else 0 for el in idle_time_line]
            result = [None] * (len(a) + len(b))
            result[::2] = a
            result[1::2] = b
            c = [i for i in result if i != 0]

        print("\nGantt_Chart:")
        for i in range(len(c)):
            print("+-----", end="--")
        print("+")

        final_mid_line = ['\t{0}\t|'.format(elem) for elem in c]
        print("|", ''.join(final_mid_line))

        for i in range(len(c)):
            print("+-----", end="--")
        print("+")
        print('\t\t'.join(str(p) for p in final_bot_line))

    def calculateUsage(self, completion_time, process_id, idle_time_line):
        """Calculates Overall CPU Usage.

        Parameters:
            completion_time (list): Data of completion times.

            process_id (list): Data of processor IDs.

            idle_time_line (list): Data of idle times.

        Returns:
            float: Calculated overall cpu usage.
        """
        processors_executed = len(process_id)
        new_idle_list = [i for i in idle_time_line if i > 0]
        wasted_time = len(new_idle_list)
        total_time = completion_time[-1:]
        for i in range(len(total_time)):
            i = int(total_time[i])
            useful_time = i - (wasted_time + (processors_executed - 1))
            cpu_usage = useful_time / i
            """
            Useful Time = Total Time - (Useless Time + (No. of Processors Executed - 1))
            Overall CPU Usage = Useful Time / Total Time
            """
            return cpu_usage

    def calcutationData(self, average_response_time, average_turnaround_time, average_waiting_time, cpu_usage):
        """Prints all calculation data.

        Prints out the data calculated from Average Response Time,
        Average Turnaround Time, Average Waiting Time, and
        Overall CPU usage

        Parameters:
            average_response_time (float): Average Response Time

            average_turnaround_time (float): Average Turnaround Time

            average_waiting_time (float): Average Waiting Time

            cpu_usage (float): Overall CPU Usage

        Returns:
            None
        """
        print("\nAverage Turnaround Time:", round(average_turnaround_time, 2), "ms")
        print("Average Response Time:", round(average_response_time, 2), "ms")
        print("Average Waiting Time:", round(average_waiting_time, 2), "ms")
        print(f'Overall CPU Usage: {"{:.2%}".format(cpu_usage)}')

class SJF:
    """Calculates Average Response Time, Average Turnaround Time,
    Average Waiting Time, Overall CPU Usage, and generates
    Gantt Chart using SJF CPU Scheduling Algorithm.

    Shortest Job First (SJF) is an OS process scheduling
    algorithm that selects for executing the waiting process with
    the smallest execution time. If two processes have the same
    length next CPU burst, then First Come will be executed.
    """
    def sortingData(self, data_processed):
        """Sorts and gets both response and completion times to a list.

        Data from schedule_data get processed into data_processed.
        Data is modified into removing the last item of the list
        "burst_time" as it is unnecessary for the SJF algorithm.
        First, the items get sorted by how SJF is supposed to and that
        is sorting by Arrival Time, if however, there happens to be
        an existing same Arrival Times that is not '0', then it will
        start to go through processing the given data from user input
        first. The '0' in as the last item for each items in the list
        represent the state of the process. When it is '0' it means
        it has not been executed while '1' means it already completed
        execution. We then get the response and completion time into
        the list through iteration separately. Data are then transferred
        to other functions within this class for them to calculate and
        make a Gantt Chart.

        Parameters:
            data_processed (list): Data transferred from schedule_data.

        Returns:
            None
        """
        data_processed.sort(key=lambda x: x[1])
        temp_modified_data = [i[:-1] for i in data_processed]
        arrival = [i[1:2] for i in temp_modified_data]

        if all(x == 0 for v in arrival for x in v):
            modified_data = temp_modified_data
            """
            If all Arrival Times are '0', then it will skip sorting.        
            """
        else:
            new_arrival = [i[1] for i in temp_modified_data]
            check_repeating = any(new_arrival.count(element) > 1 for element in new_arrival)
            """
            Above is getting Arrival Times that appear frequently.
            """
            if check_repeating is True:

                repeating_arrival = max(arrival, key=arrival.count)

                low_same_arrival = []  # List of entries with the same Arrival Times from the first sorting.
                high_same_arrival = []  # List of entries with the same Arrival Times from the second sorting.
                new_arrival_hold = []  # Temporary placement of remaining items not sorted.
                arrival_time_hold = []  # Main placement of remaining items not sorted.

                for i, j in zip(arrival, temp_modified_data):
                    if repeating_arrival == i:
                        temp_one = [j]
                        low_same_arrival.extend(temp_one)
                    else:
                        temp_two = [j]
                        arrival_time_hold.extend(temp_two)

                renew_arrival = [i[1] for i in arrival_time_hold]
                recheck_arrival = any(renew_arrival.count(element) > 1 for element in renew_arrival)
                """
                Above checks if an Arrival Time does appear frequently.
                If "False", it will skip the process of sorting.
                If "True", it will start to separate and sort out items from 
                "temp_modified_data".
                """
                if recheck_arrival is True:

                    new_repeating_arrival = max(renew_arrival, key=renew_arrival.count)
                    """
                    Above is getting Arrival Times that appear frequently again.
                    """
                    for a, b in zip(renew_arrival, arrival_time_hold):
                        if new_repeating_arrival == a:
                            new_temp_one = [b]
                            high_same_arrival.extend(new_temp_one)
                        else:
                            new_temp_two = [b]
                            new_arrival_hold.extend(new_temp_two)

                    arrival_time_hold[:] = new_arrival_hold
                """
                Above is for doing the soring again if two pairs of
                Arrival Times happen to exist.
                If "False", it will skip the process.
                If "True", it will sort the data again with the same
                procedure.                
                """
                low_arrival_burst = [i[2] for i in low_same_arrival]
                high_arrival_burst = [i[2] for i in high_same_arrival]

                sorted_low_burst = []  # Sorted items by Burst Time in first loop.
                for c, d in zip(low_arrival_burst, low_same_arrival):
                    sorted_low_burst.extend([(c, d)])
                sorted_low_burst.sort(key=lambda x: x[0])

                sorted_high_burst = []  # Sorted items by Burst Time in second loop.
                for e, f in zip(high_arrival_burst, high_same_arrival):
                    sorted_high_burst.extend([(e, f)])
                sorted_high_burst.sort(key=lambda x: x[0])

                low_burst_removed = [] # Sorted first pair and removed the Burst Time used
                for d in sorted_low_burst:
                    low_burst_removed.append(d[1])
                determine_arrival = [i[1:2] for i in low_burst_removed]
                low_arrival = min(determine_arrival[0])

                if sorted_high_burst:
                    high_burst_removed = [] # Sorted second pair and removed the Burst Time used
                    for e in sorted_high_burst:
                        high_burst_removed.append(e[1])
                    determine_arrival = [i[1:2] for i in high_burst_removed]
                    high_arrival = min(determine_arrival[0])

                modified_data = [] # Finalized data to be used in calculating and Gantt chart

                # If only two pairs exists
                if len(arrival_time_hold) == 0:
                    modified_data.extend(low_burst_removed)
                    modified_data.extend(high_burst_removed)
                    low_burst_removed.clear()
                    high_burst_removed.clear()

                # If other items and pairs exists
                elif len(arrival_time_hold) != 0:

                    first_item = [] # First processor by order
                    mid_item = [] # Second (of if only 4 processors is the Final) processor by order
                    final_item = [] # Final processor by order
                    arrival = [i[1:2] for i in temp_modified_data]
                    start_arrival = min(arrival[0]) # Takes the first arrival time

                    first_item.extend(arrival_time_hold[0])
                    arrival_time_hold.pop(0)
                    first_arrival = first_item[1]

                    # If second pair (high_arrival) exists
                    if len(sorted_high_burst) != 0 and len(sorted_low_burst) != 0 and (len(arrival) == 5 or len(arrival) == 4):
                        # If First Arrival is the Start, First -> First Pair -> Second Pair
                        if start_arrival == first_arrival:
                            temp_one = []
                            temp_one.extend(first_item)
                            modified_data.append(temp_one)
                            first_item.clear()
                            if len(first_item) == 0 and low_arrival > start_arrival:
                                modified_data.extend(low_burst_removed)
                                low_burst_removed.clear()
                                if len(low_burst_removed) == 0:
                                    modified_data.extend(high_burst_removed)
                        # If First Pair is the Start, First Pair -> First -> Second Pair
                        elif start_arrival == low_arrival:
                            modified_data.extend(low_burst_removed)
                            low_burst_removed.clear()
                            if len(low_burst_removed) == 0 and high_arrival > first_arrival:
                                temp_one = []
                                temp_one.extend(first_item)
                                modified_data.append(temp_one)
                                first_item.clear()
                                if len(first_item) == 0 and len(low_burst_removed) == 0:
                                    modified_data.extend(high_burst_removed)
                            # If Second Pair is less than First Arrival, First Pair -> Second Pair -> First
                            elif len(low_burst_removed) == 0 and first_arrival > high_arrival:
                                modified_data.extend(high_burst_removed)
                                high_burst_removed.clear()
                                if len(low_burst_removed) == 0 and len(high_burst_removed) == 0:
                                    temp_one = []
                                    temp_one.extend(first_item)
                                    modified_data.append(temp_one)

                    # If Processors are 5 or 4 and (high_arrival) does not exist
                    elif len(sorted_high_burst) == 0 and len(sorted_low_burst) != 0 and (len(arrival) == 5 or len(arrival) == 4):
                        if first_item:
                            mid_item.extend(arrival_time_hold[0])
                            arrival_time_hold.pop(0)
                            mid_arrival = mid_item[1]
                        if first_item and mid_item and arrival_time_hold:
                            final_item.extend(arrival_time_hold[0])
                            arrival_time_hold.pop(0)
                            final_arrival = final_item[1]

                    # If Processors are 3 or less
                    elif len(arrival) > 3 or len(arrival) == 3:
                        # If First Arrival is the Start, First -> Pair
                        if start_arrival == first_arrival:
                            temp_one = []
                            temp_one.extend(first_item)
                            modified_data.append(temp_one)
                            modified_data.extend(low_burst_removed)
                        # If Pair Arrival is the Start, Pair -> First
                        elif start_arrival == low_arrival:
                            modified_data.extend(low_burst_removed)
                            low_burst_removed.clear()
                            if len(low_burst_removed) == 0:
                                temp_one = []
                                temp_one.extend(first_item)
                                modified_data.append(temp_one)

                    # If Mid and Final Items exist (because there are 5 processors)
                    if len(final_item) != 0 and len(mid_item) != 0:
                        # If First Item is the Start, First -> Mid -> Pair -> Final
                        if start_arrival == first_arrival:
                            temp_one = []
                            temp_one.extend(first_item)
                            modified_data.append(temp_one)
                            first_item.clear()
                        # If First Arrival -> Mid Arrival -> Pair Arrival -> Final Arrival
                        if len(first_item) == 0 and low_arrival > mid_arrival:
                            temp_two = []
                            temp_two.extend(mid_item)
                            modified_data.append(temp_two)
                            mid_item.clear()
                            if len(mid_item) == 0 and final_arrival > low_arrival:
                                modified_data.extend(low_burst_removed)
                                low_burst_removed.clear()
                                if len(low_burst_removed) == 0 and len(mid_item) == 0:
                                    temp_three = []
                                    temp_three.extend(final_item)
                                    modified_data.append(temp_three)
                            # If First Arrival -> Mid Arrival -> Final Arrival -> Pair Arrival
                            elif len(mid_item) == 0 and low_arrival > final_arrival:
                                temp_three = []
                                temp_three.extend(final_item)
                                modified_data.append(temp_three)
                                final_item.clear()
                                if len(final_item) == 0 and len(mid_item) == 0:
                                    modified_data.extend(low_burst_removed)
                        # If First Arrival -> Pair Arrival -> Mid Arrival -> Final Arrival
                        elif len(first_item) == 0 and mid_arrival > low_arrival:
                            modified_data.extend(low_burst_removed)
                            low_burst_removed.clear()
                            if len(low_burst_removed) == 0 and final_arrival > mid_arrival:
                                temp_two = []
                                temp_two.extend(mid_item)
                                modified_data.append(temp_two)
                                mid_item.clear()
                                if len(low_burst_removed) == 0 and len(mid_item) == 0:
                                    temp_three = []
                                    temp_three.extend(final_item)
                                    modified_data.append(temp_three)
                        # If Pair Arrival is the Start, Pair -> First -> Mid -> Final
                        elif start_arrival == low_arrival:
                            modified_data.extend(low_burst_removed)
                            low_burst_removed.clear()
                            if len(low_burst_removed) == 0 and mid_arrival > first_arrival:
                                temp_one = []
                                temp_one.extend(first_item)
                                modified_data.append(temp_one)
                                first_item.clear()
                                if len(low_burst_removed) == 0 and len(first_item) == 0:
                                    temp_two = []
                                    temp_two.extend(mid_item)
                                    modified_data.append(temp_two)
                                    temp_three = []
                                    temp_three.extend(final_item)
                                    modified_data.append(temp_three)

                    # If no Final Item exists (because there are only 4 processors)
                    elif len(final_item) == 0 and len(mid_item) != 0:
                        # If First Arrival is the Start, First -> Mid -> Pair
                        if start_arrival == first_arrival:
                            temp_one = []
                            temp_one.extend(first_item)
                            modified_data.append(temp_one)
                            first_item.clear()
                            if len(first_item) == 0 and low_arrival > mid_arrival:
                                temp_two = []
                                temp_two.extend(mid_item)
                                modified_data.append(temp_two)
                                mid_item.clear()
                                if len(first_item) == 0 and len(mid_item) == 0:
                                    modified_data.extend(low_burst_removed)
                            # If First -> Pair -> Mid
                            elif len(first_item) == 0 and mid_arrival > low_arrival:
                                modified_data.extend(low_burst_removed)
                                low_burst_removed.clear()
                                if len(first_item) == 0 and len(low_burst_removed) == 0:
                                    temp_three = []
                                    temp_three.extend(mid_item)
                                    modified_data.append(temp_three)
                        # If Pair Arrival is the Start, Pair -> First -> Mid
                        elif start_arrival == low_arrival:
                            modified_data.extend(low_burst_removed)
                            low_burst_removed.clear()
                            if len(low_burst_removed) == 0 and mid_arrival > first_arrival:
                                temp_one = []
                                temp_one.extend(first_item)
                                modified_data.append(temp_one)
                                first_item.clear()
                                if len(low_burst_removed) == 0 and len(first_item) == 0:
                                    temp_two = []
                                    temp_two.extend(mid_item)
                                    modified_data.append(temp_two)

            else:

                modified_data = temp_modified_data
        """
        Sorts according to the Arrival Time and removes excess burst_time.
        If two processes have the same arrival time, it will sort
        based on Burst Times.
        """
        response_time = []
        completion_time = []
        start_value = 0

        for i in range(len(modified_data)):
            ready_queue = []  # All of the processes that have already arrived are placed here
            queue = []  # All the processes that have not arrive yet are placed here
            temp = []

            for j in range(len(modified_data)):
                if (modified_data[j][1] <= start_value) and (modified_data[j][3] == 0):
                    temp.extend([modified_data[j][0], modified_data[j][1], modified_data[j][2]])
                    ready_queue.append(temp)
                    temp = []
                elif modified_data[j][3] == 0:
                    temp.extend([modified_data[j][0], modified_data[j][1], modified_data[j][2]])
                    queue.append(temp)
                    temp = []

            if len(ready_queue) != 0:
                ready_queue.sort(key=lambda x: x[2])
                """
                Sorts the processes according to the Burst Time
                """
                response_time.append(start_value)
                start_value = start_value + ready_queue[0][2]
                end_value = start_value
                completion_time.append(end_value)
                for k in range(len(modified_data)):
                    if modified_data[k][0] == ready_queue[0][0]:
                        break
                modified_data[k][3] = 1
                modified_data[k].append(end_value)

            elif len(ready_queue) == 0:
                if start_value < queue[0][1]:
                    start_value = queue[0][1]
                response_time.append(start_value)
                start_value = start_value + queue[0][2]
                end_value = start_value
                completion_time.append(end_value)
                for k in range(len(modified_data)):
                    if modified_data[k][0] == queue[0][0]:
                        break
                modified_data[k][3] = 1
                modified_data[k].append(end_value)

        RT = SJF.calculateResponseTime(self, response_time)
        TT = SJF.calculateTurnaroundTime(self, modified_data)
        WT = SJF.calculateWaitingTime(self, modified_data)
        idle_time_line, final_bot_line = SJF.ganttChart(self, response_time, completion_time)
        CPU = SJF.calculateUsage(self, completion_time, modified_data, idle_time_line)
        SJF.printAllData(self, modified_data, response_time, completion_time)
        SJF.printGanttChart(self, modified_data, response_time, idle_time_line, final_bot_line)
        SJF.calcutationData(self, RT, TT, WT, CPU)

    def calculateResponseTime(self, response_time):
        """Calculates Average Response Time.

        Parameters:
            response_time (list): Data of response times.

        Returns:
            float: Calculated average of response times.
        """
        average_response_time = sum(response_time) / len(response_time)
        return average_response_time

    def calculateTurnaroundTime(self, modified_data):
        """Calculates Average Turnaround Time.

        Parameters:
            modified_data (list): Data modified from sortingData.

        Returns:
            float: Calculated average turnaround time.
        """
        total_turnaround_time = 0
        for i in range(len(modified_data)):
            turnaroundTime = modified_data[i][4] - modified_data[i][1]
            """
            Turnaround Time = Completion Time - Arrival Time
            """
            total_turnaround_time = total_turnaround_time + turnaroundTime
            modified_data[i].append(turnaroundTime)
        average_turnaround_time = total_turnaround_time / len(modified_data)
        return average_turnaround_time

    def calculateWaitingTime(self, modified_data):
        """Calculates Average Waiting Time.

         Parameters:
            modified_data (list): Data modified from sortingData.

        Returns:
            float: Calculated average waiting time.
    `   """
        total_waiting_time = 0
        for i in range(len(modified_data)):
            waitingTime = modified_data[i][5] - modified_data[i][2]
            """
            Waiting Time = Turnaround Time - Burst Time
            """
            total_waiting_time = total_waiting_time + waitingTime
            modified_data[i].append(waitingTime)
        average_waiting_time = total_waiting_time / len(modified_data)
        return average_waiting_time

    def printAllData(self, modified_data, response_time, completion_time):
        """Prints Out All Of The Data To Be Calculated.

        Prints Processor IDs, Arrival Time, Burst Time, Start Time, and End Time
        In a Gantt Chart form.

        Parameters:

            modified_data (list): Data modified from sortingData.

            response_time (list): Data of response times.

            completion_time (list): Data of completion times.

        Returns:
            None
        """
        id_processed = [i[0] for i in modified_data]
        arrival_time = [i[1] for i in modified_data]
        burst_time = [i[2] for i in modified_data]
        response_time = response_time[:-1]

        # Prints all IDS in Gantt Chart form
        print("\nProcess_Name:")
        for i in range(len(id_processed)):
            print("+-----", end="--")
        print("+")

        mid_line = ['\tP{0}\t|'.format(elem) for elem in id_processed]
        print("|", ''.join(mid_line))

        for i in range(len(id_processed)):
            print("+-----", end="--")
        print("+")
        print("\t", '\t\t'.join(str(p) for p in id_processed))

        # Prints all Arrival Times in Gantt Chart form
        print("\nArrival_Time:")
        for i in range(len(arrival_time)):
            print("+-----", end="--")
        print("+")

        mid_line = ['\t{0}\t|'.format(elem) for elem in arrival_time]
        print("|", ''.join(mid_line))

        for i in range(len(arrival_time)):
            print("+-----", end="--")
        print("+")
        print("\t", '\t\t'.join(str(p) for p in id_processed))

        # Prints all Burst Times in Gantt Chart form
        print("\nBurst_Time:")
        for i in range(len(burst_time)):
            print("+-----", end="--")
        print("+")

        mid_line = ['\t{0}\t|'.format(elem) for elem in burst_time]
        print("|", ''.join(mid_line))

        for i in range(len(burst_time)):
            print("+-----", end="--")
        print("+")
        print("\t", '\t\t'.join(str(p) for p in id_processed))

        # Prints all Start Times in Gantt Chart form
        print("\nStart_Time:")
        for i in range(len(response_time)):
            print("+-----", end="--")
        print("+")

        mid_line = ['\t{0}\t|'.format(elem) for elem in response_time]
        print("|", ''.join(mid_line))

        for i in range(len(response_time)):
            print("+-----", end="--")
        print("+")
        print("\t", '\t\t'.join(str(p) for p in id_processed))

        # Prints all End Times in Gantt Chart form
        print("\nEnd_Time:")
        for i in range(len(completion_time)):
            print("+-----", end="--")
        print("+")

        mid_line = ['\t{0}\t|'.format(elem) for elem in completion_time]
        print("|", ''.join(mid_line))

        for i in range(len(completion_time)):
            print("+-----", end="--")
        print("+")
        print("\t", '\t\t'.join(str(p) for p in id_processed))

    def ganttChart(self, response_time, completion_time):
        """Part One of the Gantt Chart Generation

        Gantt Chart is generated by firstly determining here whether
        the first value of the response time starts with a zero
        or numbers more than that, if the former, it will start
        by iterating through giving out an idle time line to be
        subtracted from both response and completion time.
        The resulting value is then concatenated to the list
        and forms a new response time and removes duplicates
        through final iteration and becomes the bottom line for
        the later Gantt Chart. If the latter however, the same
        method is applied except after inserting the zero at the
        start it will get the idle time which is then extended to
        the idle time line and the rest follows the same with the
        former.

        Parameters:
            response_time (list): Data of response times.

            completion_time (list): Data of completion times.

        Returns:
            idle_time_line (list): Data of idle times.

            final_bot_line (list): Data for the bottom part of the Gantt Chart
        """
        first_response_value = response_time[0:1]
        idle_time_line = []
        final_bot_line = []

        for i in range(len(first_response_value)):
            i = int(first_response_value[i])

            if i == 0:

                final_complete_value = completion_time[-1:]
                response_time.extend(final_complete_value)
                idle_time_line = [a - b for a, b in zip(response_time[1:], completion_time[0:])]
                idle_time_line.insert(0, 0)
                temp_response_time = [x - y for x, y in zip(response_time, idle_time_line)]
                new_response_time = temp_response_time + response_time
                for i in new_response_time:
                    if i not in final_bot_line:
                        final_bot_line.append(i)
                final_bot_line.sort()

            elif i != 0:

                final_complete_value = completion_time[-1:]
                response_time.extend(final_complete_value)
                response_time.insert(0, 0)
                x = response_time[:-5]
                y = response_time[1:-5]
                new_response_time = [y - x for x, y in zip(x, y)]
                idle_time_line.extend(new_response_time)
                idle_time = [a - b for a, b in zip(response_time[2:], completion_time[0:])]
                idle_time_line.extend(idle_time)
                final_bot = [a - b for a, b in zip(response_time[1:], idle_time_line)]
                response_time.extend(final_bot)
                for i in response_time:
                    if i not in final_bot_line:
                        final_bot_line.append(i)
                final_bot_line.sort()

        return idle_time_line, final_bot_line

    def printGanttChart(self, modified_data, response_time, idle_time_line, final_bot_line):
        """Part Two of the Gantt Chart Generation

        Continues synthesis and prints out the Gantt Chart
        according to the synthesized data.

        The first if-elif statement turns all of the zeroes in the
        list into 'I's which stands for "Idle".

        The second section of this function is where the Gantt Chart is
        generated.

        Parameters:
            modified_data (list):  Data modified from sortingData.

            response_time (list): Data of response times.

            idle_time_line (list): Data of idle times.

            final_bot_line (list): Data for the bottom part of the Gantt Chart

        Returns:
            None
        """
        modified_data.sort(key=lambda x: x[0])
        temp_id = modified_data.copy()
        temp_id.sort(key=lambda x: x[4])
        id = [i[0] for i in temp_id]
        """
        Sorts according to Completion Time and transfers IDs into a list copy. 
        """
        first_response_value = response_time[0:1]
        b = id
        c = []

        if first_response_value == 0:

            idle_time_line.insert(0, 0)
            a = ['I' if int(el) > 0 else 0 for el in idle_time_line]
            result = [None] * (len(a) + len(b))
            result[::1] = a
            result[0::1] = b
            c = [i for i in result if i != 0]

        elif first_response_value != 0:

            a = ['I' if int(el) > 0 else 0 for el in idle_time_line]
            result = [None] * (len(a) + len(b))
            result[::2] = a
            result[1::2] = b
            c = [i for i in result if i != 0]

        print("\nGantt_Chart:")
        for i in range(len(c)):
            print("+-----", end="--")
        print("+")

        final_mid_line = ['\t{0}\t|'.format(elem) for elem in c]
        print("|", ''.join(final_mid_line))

        for i in range(len(c)):
            print("+-----", end="--")
        print("+")
        print('\t\t'.join(str(p) for p in final_bot_line))

    def calculateUsage(self, completion_time, modified_data, idle_time_line):
        """Calculates Overall CPU Usage.

        Parameters:
            completion_time (list): Data of completion times.

            modified_data (list): (Filler)

            idle_time_line (list): Data of idle times.

        Returns:
            float: Calculated overall cpu usage.
        """
        modified_data.sort(key=lambda x: x[0])
        temp_id = modified_data.copy()
        temp_id.sort(key=lambda x: x[4])
        id = [i[0] for i in temp_id]
        """
        Sorts according to Completion Time and transfers IDs into a list copy. 
        """
        processors_executed = len(id)
        new_idle_list = [i for i in idle_time_line if i > 0]
        wasted_time = len(new_idle_list)
        total_time = completion_time[-1:]
        for i in range(len(total_time)):
            i = int(total_time[i])
            useful_time = i - (wasted_time + (processors_executed - 1))
            cpu_usage = useful_time / i
            """
            Useful Time = Total Time - (Useless Time + (No. of Processors Executed - 1))
            Overall CPU Usage = Useful Time / Total Time
            """
            return cpu_usage

    def calcutationData(self, average_response_time, average_turnaround_time, average_waiting_time, cpu_usage):
        """Prints all calculation data.

        Prints out the data calculated from Average Response Time,
        Average Turnaround Time, Average Waiting Time, and
        Overall CPU usage

        Parameters:
            average_response_time (float): Average Response Time

            average_turnaround_time (float): Average Turnaround Time

            average_waiting_time (float): Average Waiting Time

            cpu_usage (float): Overall CPU Usage

        Returns:
            None
        """
        print("\nAverage Turnaround Time:", round(average_turnaround_time, 2), "ms")
        print("Average Response Time:", round(average_response_time, 2), "ms")
        print("Average Waiting Time:", round(average_waiting_time, 2), "ms")
        print(f'Overall CPU Usage: {"{:.2%}".format(cpu_usage)}')

class SRTF:
    """Calculates Average Response Time, Average Turnaround Time,
    Average Waiting Time, Overall CPU Usage, and generates
    Gantt Chart using SRTF CPU Scheduling Algorithm.

    Shortest Remaining Time First (SRTF) is an OS process scheduling
    algorithm that is a preemptive version of shortest job next scheduling.
    The process with the smallest amount of time remaining until completion
    is selected to execute.
    """
    def sortingData(self, data_processed):
        """Sorts and gets both response and completion times to a list.

        Data from schedule_data get processed into data_processed.
        The '0' in as the last item for each items in the list
        represent the state of the process. When it is '0' it means
        it has not been executed while '1' means it already completed
        execution. We then get the sorted IDs as well as response and
        completion time into the list through iteration separately.
        We also get the ID's of the process executed by to be put through
        "process_order". Data are then transferred to other functions
        within this class for them to calculate and make a Gantt Chart.

        Parameters:
            data_processed (list): Data transferred from schedule_data.

        Returns:
            None
        """
        response_time = []
        completion_time = []
        start_value = 0
        process_order = []  # Order of processes by its execution
        data_processed.sort(key=lambda x: x[1])
        """
        Sort processes according to the Arrival Time
        """
        while True:
            ready_queue = []  # All of the processes that have already arrived are placed here
            queue = []  # All the processes that have not arrive yet are placed here
            temp = []

            for i in range(len(data_processed)):
                if data_processed[i][1] <= start_value and data_processed[i][3] == 0:
                    temp.extend(
                        [data_processed[i][0], data_processed[i][1], data_processed[i][2], data_processed[i][4]])
                    ready_queue.append(temp)
                    temp = []
                elif data_processed[i][3] == 0:
                    temp.extend(
                        [data_processed[i][0], data_processed[i][1], data_processed[i][2], data_processed[i][4]])
                    queue.append(temp)
                    temp = []
            if len(ready_queue) == 0 and len(queue) == 0:
                break
            if len(ready_queue) != 0:
                ready_queue.sort(key=lambda x: x[2])
                """
                Sorts processes according to Burst Time
                """
                response_time.append(start_value)
                start_value = start_value + 1
                end_time = start_value
                completion_time.append(end_time)
                process_order.append(ready_queue[0][0])
                for k in range(len(data_processed)):
                    if data_processed[k][0] == ready_queue[0][0]:
                        break
                data_processed[k][2] = data_processed[k][2] - 1
                if data_processed[k][2] == 0:
                    data_processed[k][3] = 1
                    data_processed[k].append(end_time)
                    """
                    If Burst Time of a process is '0', the process is completed
                    """
            if len(ready_queue) == 0:
                if start_value < queue[0][1]:
                    start_value = queue[0][1]
                response_time.append(start_value)
                start_value = start_value + 1
                end_time = start_value
                completion_time.append(end_time)
                process_order.append(queue[0][0])
                for k in range(len(data_processed)):
                    if data_processed[k][0] == queue[0][0]:
                        break
                data_processed[k][2] = data_processed[k][2] - 1
                if data_processed[k][2] == 0:
                    data_processed[k][3] = 1
                    data_processed[k].append(end_time)
                    """
                    If Burst Time of a process is '0', the process is completed
                    """

        # Takes the IDs of processes limited to represent each
        # execution once per process queued instead of every execution
        new_id = []
        value_one = 0
        for x in process_order:
            if value_one != x:
                value_one = x
                temp_one = [x]
                new_id.extend(temp_one)

        # Takes the Response Times of processes limited to represent each
        # execution once per process queued instead of every execution
        new_response_time = []
        value_two = 0
        for a, b in zip(process_order, response_time):
            if value_two != a:
                value_two = a
                temp_two = [b]
                new_response_time.extend(temp_two)

        # Takes the Completion Times of processes limited to represent each
        # execution once per process queued instead of every execution
        final_complete_time = []
        temp = []
        temp_set = set()
        for c, d in zip(reversed(process_order), reversed(completion_time)):
            if c not in temp_set:
                temp.append(c)
                temp_set.add(c)
                final_complete_time.append(d)
        final_complete_time.reverse()

        # Takes Response Times from Processed IDs only once equivalent to the number
        # of processes assigned from the user input
        final_response_time = []
        temp = []
        temp_set = set()
        for e, f in zip(new_id, new_response_time):
            if e not in temp_set:
                temp.append(e)
                temp_set.add(e)
                final_response_time.append(f)

        RT = SRTF.calculateResponseTime(self, final_response_time)
        TT = SRTF.calculateTurnaroundTime(self, data_processed)
        WT = SRTF.calculateWaitingTime(self, data_processed)
        SRTF.printAllData(self, data_processed, final_response_time)
        idle_time_line, final_bot_line = SRTF.ganttChart(self, final_response_time, final_complete_time)
        SRTF.printGanttChart(self, new_id, final_response_time, idle_time_line, final_bot_line)
        CPU = SRTF.calculateUsage(self, final_complete_time, new_id, idle_time_line)
        SRTF.calcutationData(self, RT, TT, WT, CPU)

    def calculateResponseTime(self, final_response_time):
        """Calculates Average Response Time.

        Parameters:
            final_response_time (list): Data of response times limited to user input
                                        of processes.

        Returns:
            float: Calculated average of response times.
        """
        average_response_time = sum(final_response_time) / len(final_response_time)
        return average_response_time

    def calculateTurnaroundTime(self, data_processed):
        """Calculates Average Turnaround Time.

        Parameters:
            data_processed (list): Data processed from sortingData.

        Returns:
            float: Calculated average turnaround time.
        """
        total_turnaround_time = 0
        for i in range(len(data_processed)):
            turnaroundTime = data_processed[i][5] - data_processed[i][1]
            """
            Turnaround Time = Completion Time - Arrival Time
            """
            total_turnaround_time = total_turnaround_time + turnaroundTime
            data_processed[i].append(turnaroundTime)
        average_turnaround_time = total_turnaround_time / len(data_processed)
        return average_turnaround_time

    def calculateWaitingTime(self, data_processed):
        """Calculates Average Waiting Time.

        Parameters:
            data_processed (list): Data processed from sortingData.

        Returns:
            float: Calculated average waiting time.
        """
        total_waiting_time = 0
        for i in range(len(data_processed)):
            waitingTime = data_processed[i][6] - data_processed[i][4]
            """
            Waiting Time = Turnaround Time - Burst Time
            """
            total_waiting_time = total_waiting_time + waitingTime
            data_processed[i].append(waitingTime)
        average_waiting_time = total_waiting_time / len(data_processed)
        return average_waiting_time

    def printAllData(self, data_processed, final_response_time):
        """Prints Out All Of The Data To Be Calculated.

        Prints Processor IDs, Arrival Time, Burst Time, Start Time, and End Time
        In a Gantt Chart form.

        Parameters:
            data_processed (list): Data processed from sortingData

            final_response_time (list): Data of response times limited to user input
                                        of processes.
        Returns:
            None
        """
        id_processed = [i[0] for i in data_processed]
        arrival_time = [i[1] for i in data_processed]
        burst_time = [i[4] for i in data_processed]
        complete_time = [i[5] for i in data_processed]

        # Prints all IDS in Gantt Chart form
        print("\nProcess_Name:")
        for i in range(len(id_processed)):
            print("+-----", end="--")
        print("+")

        mid_line = ['\tP{0}\t|'.format(elem) for elem in id_processed]
        print("|", ''.join(mid_line))

        for i in range(len(id_processed)):
            print("+-----", end="--")
        print("+")
        print("\t", '\t\t'.join(str(p) for p in id_processed))

        # Prints all Arrival Times in Gantt Chart form
        print("\nArrival_Time:")
        for i in range(len(arrival_time)):
            print("+-----", end="--")
        print("+")

        mid_line = ['\t{0}\t|'.format(elem) for elem in arrival_time]
        print("|", ''.join(mid_line))

        for i in range(len(arrival_time)):
            print("+-----", end="--")
        print("+")
        print("\t", '\t\t'.join(str(p) for p in id_processed))

        # Prints all Burst Times in Gantt Chart form
        print("\nBurst_Time:")
        for i in range(len(burst_time)):
            print("+-----", end="--")
        print("+")

        mid_line = ['\t{0}\t|'.format(elem) for elem in burst_time]
        print("|", ''.join(mid_line))

        for i in range(len(burst_time)):
            print("+-----", end="--")
        print("+")
        print("\t", '\t\t'.join(str(p) for p in id_processed))

        # Prints all Start Times in Gantt Chart form
        print("\nStart_Time:")
        for i in range(len(final_response_time)):
            print("+-----", end="--")
        print("+")

        mid_line = ['\t{0}\t|'.format(elem) for elem in final_response_time]
        print("|", ''.join(mid_line))

        for i in range(len(final_response_time)):
            print("+-----", end="--")
        print("+")
        print("\t", '\t\t'.join(str(p) for p in id_processed))

        # Prints all End Times in Gantt Chart form
        print("\nEnd_Time:")
        for i in range(len(complete_time)):
            print("+-----", end="--")
        print("+")

        mid_line = ['\t{0}\t|'.format(elem) for elem in complete_time]
        print("|", ''.join(mid_line))

        for i in range(len(complete_time)):
            print("+-----", end="--")
        print("+")
        print("\t", '\t\t'.join(str(p) for p in id_processed))

    def ganttChart(self, final_response_time, final_complete_time):
        """Part One of the Gantt Chart Generation

        Gantt Chart is generated by firstly determining here whether
        the first value of the response time starts with a zero
        or numbers more than that, if the former, it will start
        by iterating through giving out an idle time line to be
        subtracted from both response and completion time.
        The resulting value is then concatenated to the list
        and forms a new response time and removes duplicates
        through final iteration and becomes the bottom line for
        the later Gantt Chart. If the latter however, the same
        method is applied except after inserting the zero at the
        start it will get the idle time which is then extended to
        the idle time line and the rest follows the same with the
        former.

        Parameters:
            final_response_time (list): Data of response times limited to user input
                                        of processes.

            final_complete_time (list): Data of completion times.

        Returns:
            idle_time_line (list): Data of idle times.

            final_bot_line (list): Data for the bottom part of the Gantt Chart
        """
        first_response_value = final_response_time[0:1]
        idle_time_line = []
        final_bot_line = []

        for i in range(len(first_response_value)):
            i = int(first_response_value[i])

            if i == 0:

                final_complete_value = final_complete_time[-1:]
                final_response_time.extend(final_complete_value)
                idle_time_line = [a - b for a, b in zip(final_response_time[1:], final_complete_time[0:])]
                idle_time_line.insert(0, 0)
                temp_resp_time = [x - y for x, y in zip(final_response_time, idle_time_line)]
                new_resp_time = temp_resp_time + final_response_time
                for i in new_resp_time:
                    if i not in final_bot_line:
                        final_bot_line.append(i)
                final_bot_line.sort()

            elif i != 0:

                final_complete_value = final_complete_time[-1:]
                final_response_time.extend(final_complete_value)
                final_response_time.insert(0, 0)
                x = final_response_time[:-5]
                y = final_response_time[1:-5]
                new_resp_time = [y - x for x, y in zip(x, y)]
                idle_time_line.extend(new_resp_time)
                idle_time = [a - b for a, b in zip(final_response_time[2:], final_complete_time[0:])]
                idle_time_line.extend(idle_time)
                final_bot = [a - b for a, b in zip(final_response_time[1:], idle_time_line)]
                final_response_time.extend(final_bot)
                for i in final_response_time:
                    if i not in final_bot_line:
                        final_bot_line.append(i)
                final_bot_line.sort()

        return idle_time_line, final_bot_line

    def printGanttChart(self, new_id, final_response_time, idle_time_line, final_bot_line):
        """Part Two of the Gantt Chart Generation

        Continues synthesis and prints out the Gantt Chart
        according to the synthesized data.

        The first if-elif statement turns all of the zeroes in the
        list into 'I's which stands for "Idle".

        The second section of this function is where the Gantt Chart is
        generated.

        Parameters:
            new_id (list): IDs of processes limited to represent each
                           execution once per process queued instead
                           of every execution.

            final_response_time (list): Data of response times limited to user input
                                        of processes.

            idle_time_line (list): Data of idle times.

            final_bot_line (list): Data for the bottom part of the Gantt Chart

        Returns:
            None
        """
        first_response_value = final_response_time[0:1]
        b = new_id
        c = []

        if first_response_value != 0:

            a = ['I' if int(el) > 0 else 0 for el in idle_time_line]
            result = [None] * (len(a) + len(b))
            result[::1] = a
            result[0::1] = b
            c = [i for i in result if i != 0]

        elif first_response_value == 0:

            idle_time_line.insert(0, 0)
            a = ['I' if int(el) > 0 else 0 for el in idle_time_line]
            result = [None] * (len(a) + len(b))
            result[::2] = a
            result[1::2] = b
            c = [i for i in result if i != 0]

        print("\nGantt_Chart:")
        for i in range(len(c)):
            print("+-----", end="--")
        print("+")

        final_mid_line = ['\t{0}\t|'.format(elem) for elem in c]
        print("|", ''.join(final_mid_line))

        for i in range(len(c)):
            print("+-----", end="--")
        print("+")
        print('\t\t'.join(str(p) for p in final_bot_line))

    def calculateUsage(self, final_complete_time, new_id, idle_time_line):
        """Calculates Overall CPU Usage.

        Parameters:
            final_complete_time (list): Completion Times of processes limited
                                        to represent each execution once per
                                        process queued instead of every execution

            new_id (list): IDs of processes limited to represent each
                           execution once per process queued instead
                           of every execution.

            idle_time_line (list): Data of idle times.

        Returns:
            float: Calculated overall cpu usage.
        """
        processors_executed = len(new_id)
        new_idle_list = [i for i in idle_time_line if i > 0]
        wasted_time = len(new_idle_list)
        total_time = final_complete_time[-1:]
        for i in range(len(total_time)):
            i = int(total_time[i])
            useful_time = i - (wasted_time + (processors_executed - 1))
            cpu_usage = useful_time / i
            """
            Useful Time = Total Time - (Useless Time + (No. of Processors Executed - 1))
            Overall CPU Usage = Useful Time / Total Time
            """
            return cpu_usage

    def calcutationData(self, average_response_time, average_turnaround_time, average_waiting_time, cpu_usage):
        """Prints all calculation data.

        Prints out the data calculated from Average Response Time,
        Average Turnaround Time, Average Waiting Time, and
        Overall CPU usage

        Parameters:
            average_response_time (float): Average Response Time

            average_turnaround_time (float): Average Turnaround Time

            average_waiting_time (float): Average Waiting Time

            cpu_usage (float): Overall CPU Usage

        Returns:
            None
        """
        print("\nAverage Turnaround Time:", round(average_turnaround_time, 2), "ms")
        print("Average Response Time:", round(average_response_time, 2), "ms")
        print("Average Waiting Time:", round(average_waiting_time, 2), "ms")
        print(f'Overall CPU Usage: {"{:.2%}".format(cpu_usage)}')

class RR:
    """Calculates Average Response Time, Average Turnaround Time,
    Average Waiting Time, Overall CPU Usage, and generates
    Gantt Chart using RR CPU Scheduling Algorithm.

    Round Robin (RR) is an OS process scheduling algorithm that
    uses time slices that are assigned to each processes in the
    queue or line. Each process is allowed to use CPU for a given
    amount of time. If it does not finish within the allotted time,
    then it is preempted and moved at the back of the line so that
    the next process in line is able to use the CPU for the same
    amount of time.
    """
    def timeSlice(self, data_processed):
        """Gets The Time Slice From User.

        A time slice is short time frame that
        gets assigned to process for CPU execution

        Parameters:
            data_processed (list): Data transferred from schedule_data.

        Returns:
            data_processed (list): Data transferred from schedule_data.

            time_slice (int): Time slice gathered from the user.
        """
        while True:
            try:
                time_slice = int(input("\nEnter Time Slice: "))
            except ValueError:
                print("\nError! Please only input numbers for Time Slice!")
                continue
            if 0 >= time_slice:
                print("\nError! Please don't input negatives or zero for Time Slice!")
                continue
            else:
                break

        RR.sortingData(self, data_processed, time_slice)

    def sortingData(self, data_processed, time_slice):
        """Sorts and gets both response and completion times to a list.

        Data from schedule_data get processed into data_processed.
        The '0' in as the last item for each items in the list
        represent the state of the process. When it is '0' it means
        it has not been executed while '1' means it already completed
        execution. We then get the sorted IDs as well as response and
        completion time into the list through iteration separately.
        We also get the ID's of the process executed by to be put through
        "process_order". Data are then transferred to other functions
        within this class for them to calculate and make a Gantt Chart.

        Parameters:
            data_processed (list): Data transferred from schedule_data.

            time_slice (int): Time slice gathered from the user.

        Returns:
            None
        """
        response_time = []
        complete_time = []
        process_order = []  # Order of processes by its execution
        ready_queue = []  # All of the processes that have already arrived are placed here
        start_value = 0
        data_processed.sort(key=lambda x: x[1])
        """
        Sorts processes according to the Arrival Time.
        """
        while True:
            queue = []  # All the processes that have not arrive yet are placed here
            temp = []
            for i in range(len(data_processed)):
                if data_processed[i][1] <= start_value and data_processed[i][3] == 0:
                    present = 0
                    if len(ready_queue) != 0:
                        for k in range(len(ready_queue)):
                            if data_processed[i][0] == ready_queue[k][0]:
                                present = 1
                    """
                    The above if loop checks that the next process is not a part of ready_queue.
                    """
                    if present == 0:
                        temp.extend(
                            [data_processed[i][0], data_processed[i][1], data_processed[i][2], data_processed[i][4]])
                        ready_queue.append(temp)
                        temp = []
                    """
                    The above if loop adds a process to the ready_queue only if it is not already present in it.
                    """
                    if len(ready_queue) != 0 and len(process_order) != 0:
                        for k in range(len(ready_queue)):
                            if ready_queue[k][0] == process_order[len(process_order) - 1]:
                                ready_queue.insert((len(ready_queue) - 1), ready_queue.pop(k))
                    """
                    The above if loop makes sure that the recently executed process is appended at the end of ready_queue.
                    """
                elif data_processed[i][3] == 0:
                    temp.extend(
                        [data_processed[i][0], data_processed[i][1], data_processed[i][2], data_processed[i][4]])
                    queue.append(temp)
                    temp = []
            if len(ready_queue) == 0 and len(queue) == 0:
                break
            if len(ready_queue) != 0:
                if ready_queue[0][2] > time_slice:
                    """
                    If process has remaining burst time greater than the time slice, it will execute for a time period equal to time slice and then switch.
                    """
                    response_time.append(start_value)
                    start_value = start_value + time_slice
                    exit_value = start_value
                    complete_time.append(exit_value)
                    process_order.append(ready_queue[0][0])
                    for j in range(len(data_processed)):
                        if data_processed[j][0] == ready_queue[0][0]:
                            break
                    data_processed[j][2] = data_processed[j][2] - time_slice
                    ready_queue.pop(0)
                elif ready_queue[0][2] <= time_slice:
                    """
                    If a process has a remaining burst time less than or equal to time slice, it will complete its execution.
                    """
                    response_time.append(start_value)
                    start_value = start_value + ready_queue[0][2]
                    exit_value = start_value
                    complete_time.append(exit_value)
                    process_order.append(ready_queue[0][0])
                    for j in range(len(data_processed)):
                        if data_processed[j][0] == ready_queue[0][0]:
                            break
                    data_processed[j][2] = 0
                    data_processed[j][3] = 1
                    data_processed[j].append(exit_value)
                    ready_queue.pop(0)
            elif len(ready_queue) == 0:
                if start_value < queue[0][1]:
                    start_value = queue[0][1]
                if queue[0][2] > time_slice:
                    """
                    If process has remaining burst time greater than the time slice, it will execute for a time period equal to time slice and then switch.
                    """
                    response_time.append(start_value)
                    start_value = start_value + time_slice
                    exit_value = start_value
                    complete_time.append(exit_value)
                    process_order.append(queue[0][0])
                    for j in range(len(data_processed)):
                        if data_processed[j][0] == queue[0][0]:
                            break
                    data_processed[j][2] = data_processed[j][2] - time_slice
                elif queue[0][2] <= time_slice:
                    """
                    If a process has a remaining burst time less than or equal to time slice, it will complete its execution.
                    """
                    response_time.append(start_value)
                    start_value = start_value + queue[0][2]
                    exit_value = start_value
                    complete_time.append(exit_value)
                    process_order.append(queue[0][0])
                    for j in range(len(data_processed)):
                        if data_processed[j][0] == queue[0][0]:
                            break
                    data_processed[j][2] = 0
                    data_processed[j][3] = 1
                    data_processed[j].append(exit_value)

        # Takes the IDs of processes limited to represent each
        # execution once per process queued instead of every execution
        new_id = []
        value_one = 0
        for x in process_order:
            if value_one != x:
                value_one = x
                temp_one = [x]
                new_id.extend(temp_one)

        # Takes the Response Times of processes limited to represent each
        # execution once per process queued instead of every execution
        new_response_time = []
        value_two = 0
        for a, b in zip(process_order, response_time):
            if value_two != a:
                value_two = a
                temp_two = [b]
                new_response_time.extend(temp_two)

        # Takes the Completion Times of processes limited to represent each
        # execution once per process queued instead of every execution
        final_complete_time = []
        value_three = 0
        for h, i in zip(reversed(process_order), reversed(complete_time)):
            if value_three != h:
                value_three = h
                temp_three = [i]
                final_complete_time.extend(temp_three)
        final_complete_time.reverse()

        # Takes Response Times from Processed IDs only once equivalent to the number
        # of processes assigned from the user input
        final_response_time = []
        temp = []
        temp_set = set()
        for e, f in zip(new_id, new_response_time):
            if e not in temp_set:
                temp.append(e)
                temp_set.add(e)
                final_response_time.append(f)

        RT = RR.calculateResponseTime(self, final_response_time)
        TT = RR.calculateTurnaroundTime(self, data_processed)
        WT = RR.calculateWaitingTime(self, data_processed)
        RR.printAllData(self, data_processed, final_response_time)
        idle_time_line, final_bot_line = RR.ganttChart(self, new_response_time, final_complete_time)
        RR.printGanttChart(self, new_response_time, new_id, idle_time_line, final_bot_line)
        CPU = RR.calculateUsage(self, final_complete_time, new_id, idle_time_line)
        RR.calcutationData(self, RT, TT, WT, CPU)

    def calculateResponseTime(self, final_response_time):
        """Calculates Average Response Time.

        Parameters:
            final_response_time (list): Data of response times limited to user input
                                        of processes.

        Returns:
            float: Calculated average of response times.
        """
        average_response_time = sum(final_response_time) / len(final_response_time)
        return average_response_time

    def calculateTurnaroundTime(self, data_processed):
        """Calculates Average Turnaround Time.

        Parameters:
            data_processed (list): Data processed from sortingData.

        Returns:
            float: Calculated average turnaround time.
        """
        total_turnaround_time = 0
        for i in range(len(data_processed)):
            turnaroundTime = data_processed[i][5] - data_processed[i][1]
            """
            Turnaround Time = Completion Time - Arrival Time
            """
            total_turnaround_time = total_turnaround_time + turnaroundTime
            data_processed[i].append(turnaroundTime)
        average_turnaround_time = total_turnaround_time / len(data_processed)
        return average_turnaround_time

    def calculateWaitingTime(self, data_processed):
        """Calculates Average Waiting Time.

        Parameters:
            data_processed (list): Data processed from sortingData.

        Returns:
            float: Calculated average waiting time.
        """
        total_waiting_time = 0
        for i in range(len(data_processed)):
            waitingTime = data_processed[i][6] - data_processed[i][4]
            """
            Waiting Time = Turnaround Time - Burst Time
            """
            total_waiting_time = total_waiting_time + waitingTime
            data_processed[i].append(waitingTime)
        average_waiting_time = total_waiting_time / len(data_processed)
        return average_waiting_time

    def printAllData(self, data_processed, final_response_time):
        """Prints Out All Of The Data To Be Calculated.

        Prints Processor IDs, Arrival Time, Burst Time, Start Time, and End Time
        In a Gantt Chart form.

        Parameters:
            data_processed (list): Data processed from sortingData

            final_response_time (list): Data of response times limited to user input
                                                of processes.
        Returns:
            None
        """
        id_processed = [i[0] for i in data_processed]
        arrival_time = [i[1] for i in data_processed]
        burst_time = [i[4] for i in data_processed]
        complete_time = [i[5] for i in data_processed]

        # Prints all IDS in Gantt Chart form
        print("\nProcess_Name:")
        for i in range(len(id_processed)):
            print("+-----", end="--")
        print("+")

        mid_line = ['\tP{0}\t|'.format(elem) for elem in id_processed]
        print("|", ''.join(mid_line))

        for i in range(len(id_processed)):
            print("+-----", end="--")
        print("+")
        print("\t", '\t\t'.join(str(p) for p in id_processed))

        # Prints all Arrival Times in Gantt Chart form
        print("\nArrival_Time:")
        for i in range(len(arrival_time)):
            print("+-----", end="--")
        print("+")

        mid_line = ['\t{0}\t|'.format(elem) for elem in arrival_time]
        print("|", ''.join(mid_line))

        for i in range(len(arrival_time)):
            print("+-----", end="--")
        print("+")
        print("\t", '\t\t'.join(str(p) for p in id_processed))

        # Prints all Burst Times in Gantt Chart form
        print("\nBurst_Time:")
        for i in range(len(burst_time)):
            print("+-----", end="--")
        print("+")

        mid_line = ['\t{0}\t|'.format(elem) for elem in burst_time]
        print("|", ''.join(mid_line))

        for i in range(len(burst_time)):
            print("+-----", end="--")
        print("+")
        print("\t", '\t\t'.join(str(p) for p in id_processed))

        # Prints all Start Times in Gantt Chart form
        print("\nStart_Time:")
        for i in range(len(final_response_time)):
            print("+-----", end="--")
        print("+")

        mid_line = ['\t{0}\t|'.format(elem) for elem in final_response_time]
        print("|", ''.join(mid_line))

        for i in range(len(final_response_time)):
            print("+-----", end="--")
        print("+")
        print("\t", '\t\t'.join(str(p) for p in id_processed))

        # Prints all End Times in Gantt Chart form
        print("\nEnd_Time:")
        for i in range(len(complete_time)):
            print("+-----", end="--")
        print("+")

        mid_line = ['\t{0}\t|'.format(elem) for elem in complete_time]
        print("|", ''.join(mid_line))

        for i in range(len(complete_time)):
            print("+-----", end="--")
        print("+")
        print("\t", '\t\t'.join(str(p) for p in id_processed))

    def ganttChart(self, new_response_time, final_complete_time):
        """Part One of the Gantt Chart Generation

        Gantt Chart is generated by firstly determining here whether
        the first value of the response time starts with a zero
        or numbers more than that, if the former, it will start
        by iterating through giving out an idle time line to be
        subtracted from both response and completion time.
        The resulting value is then concatenated to the list
        and forms a new response time and removes duplicates
        through final iteration and becomes the bottom line for
        the later Gantt Chart. If the latter however, the same
        method is applied except after inserting the zero at the
        start it will get the idle time which is then extended to
        the idle time line and the rest follows the same with the
        former.

        Parameters:
            new_response_time (list): Response Times of processes limited
                                      to represent each execution once per
                                      process queued instead of every execution.

            final_complete_time (list): Data of completion times.

        Returns:
            idle_time_line (list): Data of idle times.

            final_bot_line (list): Data for the bottom part of the Gantt Chart
        """
        first_response_value = new_response_time[0:1]
        idle_time_line = []
        final_bot_line = []

        for i in range(len(first_response_value)):
            i = int(first_response_value[i])

            if i == 0:
                final_val = final_complete_time[-1:]
                new_response_time.extend(final_val)
                idle_time_line = [a - b for a, b in zip(new_response_time[1:], final_complete_time[0:])]
                idle_time_line.insert(0, 0)
                temp_resp_time = [x - y for x, y in zip(new_response_time, idle_time_line)]
                new_resp_time = temp_resp_time + new_response_time
                for i in new_resp_time:
                    if i not in final_bot_line:
                        final_bot_line.append(i)
                final_bot_line.sort()

            elif i != 0:
                final_val = final_complete_time[-1:]
                new_response_time.extend(final_val)
                new_response_time.insert(0, 0)
                x = new_response_time[:-5]
                y = new_response_time[1:-5]
                new_resp_time = [y - x for x, y in zip(x, y)]
                idle_time_line.extend(new_resp_time)
                idle_time = [a - b for a, b in zip(new_response_time[2:], final_complete_time[0:])]
                idle_time_line.extend(idle_time)
                final_bot = [a - b for a, b in zip(new_response_time[1:], idle_time_line)]
                new_response_time.extend(final_bot)
                for i in new_response_time:
                    if i not in final_bot_line:
                        final_bot_line.append(i)
                final_bot_line.sort()

        return idle_time_line, final_bot_line

    def printGanttChart(self, new_response_time, new_id, idle_time_line, final_bot_line):
        """Part Two of the Gantt Chart Generation

        Continues synthesis and prints out the Gantt Chart
        according to the synthesized data.

        The first if-elif statement turns all of the zeroes in the
        list into 'I's which stands for "Idle".

        The second section of this function is where the Gantt Chart is
        generated.

        Parameters:
            new_id (list): IDs of processes limited to represent each
                           execution once per process queued instead
                           of every execution.

            new_response_time (list): Response Times of processes limited
                                      to represent each execution once per
                                      process queued instead of every execution.

            idle_time_line (list): Data of idle times.

            final_bot_line (list): Data for the bottom part of the Gantt Chart

        Returns:
            None
        """
        first_response_value = new_response_time[0:1]
        b = new_id
        c = []

        if first_response_value != 0:
            a = ['I' if int(el) > 0 else 0 for el in idle_time_line]
            result = [None] * (len(a) + len(b))
            result[::2] = a
            result[1::2] = b
            c = [i for i in result if i != 0]

        elif first_response_value == 0:
            idle_time_line.insert(0, 0)
            a = ['I' if int(el) > 0 else 0 for el in idle_time_line]
            result = [None] * (len(a) + len(b))
            result[::1] = a
            result[0::1] = b
            c = [i for i in result if i != 0]

        print("\nGantt Chart:")
        for i in range(len(c)):
            print("+-----", end="--")
        print("+")

        mid = ['\t{0}\t|'.format(elem) for elem in c]
        print("|", ''.join(mid))

        for i in range(len(c)):
            print("+-----", end="--")
        print("+")
        print('\t\t'.join(str(p) for p in final_bot_line))

    def calculateUsage(self, final_complete_time, new_id, idle_time_line):
        """Calculates Overall CPU Usage.

        Parameters:
            final_complete_time (list): Completion Times of processes limited
                                        to represent each execution once per
                                        process queued instead of every execution

            new_id (list): IDs of processes limited to represent each
                           execution once per process queued instead
                           of every execution.

            idle_time_line (list): Data of idle times.

        Returns:
            float: Calculated overall cpu usage.
        """
        processors_executed = len(new_id)
        new_idle_list = [i for i in idle_time_line if i > 0]
        wasted_time = len(new_idle_list)
        total_time = final_complete_time[-1:]
        for i in range(len(total_time)):
            i = int(total_time[i])
            useful_time = i - (wasted_time + (processors_executed - 1))
            cpu_usage = useful_time / i
            """
            Useful Time = Total Time - (Useless Time - (No. of Processors Executed - 1))
            Overall CPU Usage = Useful Time / Total Time
            """
            return cpu_usage

    def calcutationData(self, average_response_time, average_turnaround_time, average_waiting_time, cpu_usage):
        """Prints all calculation data.

        Prints out the data calculated from Average Response Time,
        Average Turnaround Time, Average Waiting Time, and
        Overall CPU usage

        Parameters:
            average_response_time (float): Average Response Time

            average_turnaround_time (float): Average Turnaround Time

            average_waiting_time (float): Average Waiting Time

            cpu_usage (float): Overall CPU Usage

        Returns:
            None
        """
        print("\nAverage Turnaround Time:", round(average_turnaround_time, 2), "ms")
        print("Average Response Time:", round(average_response_time, 2), "ms")
        print("Average Waiting Time:", round(average_waiting_time, 2), "ms")
        print(f'Overall CPU Usage: {"{:.2%}".format(cpu_usage)}')

if __name__ == "__main__":

    def getData(some_str: str = None):
        """Section gathers data from the user.

        Parameters:
            some_str (str): No description.

        Returns:
            schedule_input (list): List that contains user input.
        """
        while True:
            try:
                process_no = int(input("Number of Processes [Max: 5]: "))
            except ValueError:
                print("\nError! Only 1-5 processes are allowed!\n")
                continue
            if process_no <= 0 or process_no >= 6:
                print("\nError! Please don't put negative, zero, or numbers more than 6!\n")
                continue
            else:
                schedule_input = []
                for i in range(process_no):
                    placeholder = []

                    while True:
                        try:
                            process_id = int(input("\nEnter Process ID: "))
                        except ValueError:
                            print("\nError! Please only input numbers for IDs!")
                            continue
                        if 0 >= process_id:
                            print("\nError! Please don't use zeroes or negatives for IDs!")
                            continue
                        else:
                            break

                    while True:
                        try:
                            arrival_time = int(input(f'Enter Arrival for ID #{process_id}: '))
                        except ValueError:
                            print("\nError! Please only input numbers for Arrival Time!\n")
                            continue
                        if 0 > arrival_time:
                            print("\nError! Please don't input negatives for Arrival Time!\n")
                            continue
                        else:
                            break

                    while True:
                        try:
                            burst_time = int(input(f'Enter Burst Time for ID #{process_id}: '))
                        except ValueError:
                            print("\nError! Please only input numbers for Burst Time!\n")
                            continue
                        if 0 > burst_time:
                            print("\nError! Please don't input negatives for Burst Time!\n")
                            continue
                        else:
                            break

                    placeholder.extend([process_id, arrival_time, burst_time, 0, burst_time])
                    schedule_input.append(placeholder)
                return schedule_input

    schedule_data = getData()

    def getType():
        while True:
            try:
                input_schedule_type = input(
                    "\nEnter Schedule Type [Type A-D only] (A: FCFS, B: SJF, C: SRTF, and D: RR): ")
            except:
                break
            if input_schedule_type.islower():
                print("\nError! Please enter a valid input! Make sure the letter selected is capitalized!")
                continue
            else:
                if input_schedule_type == "A":
                    fcfs = FCFS()
                    fcfs.sortingData(schedule_data)
                elif input_schedule_type == "B":
                    sjf = SJF()
                    sjf.sortingData(schedule_data)
                elif input_schedule_type == "C":
                    srtf = SRTF()
                    srtf.sortingData(schedule_data)
                elif input_schedule_type == "D":
                    rr = RR()
                    rr.timeSlice(schedule_data)
                else:
                    print("\nError! Please enter a valid input! Make sure it is capitalized and the appropriate type!")
                    continue
            return input_schedule_type

    getType()
