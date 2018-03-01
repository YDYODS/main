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
        self.vehicles = [Vehicle(total_steps) for x in range(self.total_cars)]

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


class Vehicle(object):

    def __init__(self, total_steps) -> None:
        self.remaining = total_steps
        self.pos = [0, 0]
        self.rides = []

    def move(self, target_pos):
        self.remaining -= abs(self.pos[0] - target_pos[0]) + abs(self.pos[1] - target_pos[1])
        self.pos = target_pos


class Parser(object):
    @staticmethod
    def distance_from_to(from_data, to_data):
        return abs(from_data[0] - to_data[0]) + abs(from_data[1] - to_data[1])

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

        simulation.rides = sorted(simulation.rides, key=lambda ride: (ride.start_time, ride.distance))

        # vehicle_index = 0
        # for ride in simulation.rides:
        #     if sum(obj.distance for obj in simulation.vehicles[vehicle_index]) >= simulation.total_steps:
        #         vehicle_index += 1
        #     if vehicle_index >= len(simulation.vehicles):
        #         break
        #     simulation.vehicles[vehicle_index].append(ride)
        #
        # ride_index = 0
        # while ride_index < len(simulation.rides):
        #     should_be_done = ride_index
        #     for vehicle in simulation.vehicles:
        #         simulation.rides = sorted(simulation.rides, key=lambda ride: (ride.start_time, Parser.distance_from_to(vehicle.pos, ride.start)))
        #         if ride_index >= len(simulation.rides):
        #             break
        #         current_ride = simulation.rides[ride_index]
        #
        #         ride_price = Parser.distance_from_to(vehicle.pos, current_ride.start) + current_ride.distance
        #         step = simulation.total_steps - vehicle.remaining
        #         if vehicle.remaining <= ride_price or current_ride.start_time <= step + Parser.distance_from_to(vehicle.pos, current_ride.start) or current_ride.end_time <= ride_price + step:
        #             continue
        #         if vehicle.pos != current_ride.start:
        #             vehicle.move(current_ride.start)
        #         vehicle.rides.append(current_ride)
        #         vehicle.move(current_ride.end)
        #         if vehicle.remaining >= simulation.total_steps:
        #             continue
        #         ride_index += 1
        #     if ride_index == should_be_done:
        #         ride_index += 1

        tmp_rides = simulation.rides
        for vehicle in simulation.vehicles:
            ride_index_2 = 0
            while vehicle.remaining > 0:
                if len(tmp_rides) == 0 or ride_index_2 >= len(tmp_rides):
                    break
                current_ride = sorted(tmp_rides, key=lambda ride: (Parser.distance_from_to(vehicle.pos, ride.start), ride.start_time))[ride_index_2]

                ride_price = Parser.distance_from_to(vehicle.pos, current_ride.start) + current_ride.distance
                step = simulation.total_steps - vehicle.remaining
                if vehicle.remaining <= ride_price or current_ride.start_time <= step + Parser.distance_from_to(vehicle.pos, current_ride.start) or current_ride.end_time <= ride_price + step:
                    ride_index_2 += 1
                    continue
                if vehicle.pos != current_ride.start:
                    vehicle.move(current_ride.start)
                vehicle.rides.append(current_ride)
                vehicle.move(current_ride.end)
                if vehicle.remaining >= simulation.total_steps:
                    continue
                tmp_rides.pop(0)
            if len(tmp_rides) == 0 or ride_index_2 >= len(tmp_rides):
                break

    @staticmethod
    def output(filename):
        global simulation
        output = open(filename, 'w')

        for idx, vehicle in enumerate(simulation.vehicles):
            out = '{} {}\n'.format(len(vehicle.rides), ' '.join([str(obj.id) for obj in vehicle.rides]))
            output.write(out)

        output.close()
