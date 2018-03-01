simulation = None


class Simulation(object):
    def __init__(self, rows, columns, total_cars, total_rides, bonus, total_steps) -> None:
        super().__init__()
        self.rows = rows
        self.columns = columns
        self.total_cars = total_cars
        self.total_rides = total_rides
        self.bonus = bonus
        self.total_steps = total_steps
        self.rides = []
        self.vehicles = [[] for x in range(self.total_cars)]

    def add_ride(self, ride):
        self.rides.append(ride)


class Ride(object):
    def __init__(self, id, start, end, start_time, end_time) -> None:
        super().__init__()
        self.id = id
        self.start = start
        self.end = end
        self.start_time = start_time
        self.end_time = end_time
        self.distance = abs(start[0] - end[0]) + abs(start[1] - end[1])
        self.distance_from_start = abs(0 - start[0]) + abs(0 - start[1])

    def __str__(self) -> str:
        return "start: {}, end: {}".format(self.start, self.end)

    def __repr__(self):
        return "start: {}, end: {}".format(self.start, self.end)


class Parser(object):
    @staticmethod
    def parse(filename):
        global simulation

        file = open(filename)
        all_lines = file.readlines()
        first_line = [int(x) for x in all_lines[0].split(' ')]
        simulation = Simulation(first_line[0], first_line[1], first_line[2], first_line[3], first_line[4], first_line[5])

        rides = all_lines[1:]
        for index, line in enumerate(rides):
            line_splitted = [int(x) for x in line.split(' ')]
            ride = Ride(index, [line_splitted[0], line_splitted[1]], [line_splitted[2], line_splitted[3]], line_splitted[4], line_splitted[5])
            if max(ride.distance_from_start, ride.start_time) + ride.distance < simulation.total_steps:
                simulation.add_ride(ride)

        simulation.rides = sorted(simulation.rides, key=lambda ride: ride.distance_from_start)

        vehicle_index = 0
        for ride in simulation.rides:
            if sum(obj.distance for obj in simulation.vehicles[vehicle_index]) >= simulation.total_steps:
                vehicle_index += 1
            if vehicle_index >= len(simulation.vehicles):
                break
            simulation.vehicles[vehicle_index].append(ride)



    @staticmethod
    def output(filename):
        global simulation
        output = open(filename, 'w')

        for vehicle in simulation.vehicles:
            out = '{} {}\n'.format(len(vehicle), ' '.join([str(obj.id) for obj in vehicle]))
            output.write(out)

        output.close()