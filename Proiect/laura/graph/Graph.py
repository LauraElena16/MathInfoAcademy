import queue
import os

class NodeDetails:
    def __init__(self, x, y, label, node_type, no_room, details, floor):
        self.x: float = x
        self.y: float = y
        self.label: int = label
        self.node_type: str = node_type
        self.no_room: str = no_room
        self.details: str = details
        self.floor: int = floor


class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


class Graph(Singleton):
    def __init__(self, file_path=None):
        if not hasattr(self, 'num_nodes'):
            if file_path is None:
                dir_path = os.path.dirname(os.path.realpath(__file__))
                file_path = os.path.join(dir_path, 'graph.txt')
                
            self.num_nodes: int = 0
            self.adj: dict[int, list[int]] = {}
            self.info: dict[int, NodeDetails] = {}
            self.num_nodes, self.adj, self.info = self.__load_graph(file_path)


    def __format_string(self, string):
        return string.replace("_", " ")


    def __load_graph(self, file_path): 
        with open(file_path, "r") as file:
            num_nodes = int(file.readline().strip())
            info = {}
            adj = {}
            for _ in range(num_nodes):
                all_details = file.readline().strip().split()
                x, y = map(float, all_details[:2])
                label = int(all_details[2])
                node_type = all_details[3]
                no_room = None
                details = None
                floor = None
                if node_type == "s":
                    no_room = self.__format_string(all_details[4])
                    if len(all_details) == 6:
                        details = self.__format_string(all_details[5])
                elif node_type == "he":
                    floor = int(all_details[4])
                    details = self.__format_string(all_details[5])
                info[label] = NodeDetails(x, y, label, node_type, no_room, details, floor)
                adj[label] = []

            for line in file:
                first, second = map(int, line.split())
                adj[first].append(second)
                adj[second].append(first)
        
        return num_nodes, adj, info
    
    def find_min_path(self, start, finish):
        q = queue.Queue()
        viz = {label : False for label in self.adj.keys()}
        q.put([start, [start]])
        
        while not q.empty():
            curr_node, curr_path = q.get()

            if viz[curr_node]:
                continue

            viz[curr_node] = True
            if curr_node == finish:
                return curr_path
            
            for next_node in self.adj[curr_node]:
                if not viz[next_node]:
                    q.put([next_node, curr_path + [next_node]])

                    

    def get_directions_for_path(self, path: list[int]) -> list[str]:
        directions = []
        steer_mapping = {-1: "right", 1: "left", 0: "straight ahead"}
        floor_directions = {1: "up", -1: "down"}
        floor_mapping = {
            -1: "Basement",
            0: "Ground",
            1: "First",
            2: "Second",
            3: "Third",
            4: "Fourth",
        }
        
        if self.info[path[0]].node_type == 's':
            start_node = self.info[path[0]]
            try:
                if 'entrance' in start_node.details.lower():
                    directions.append("Enter the faculty")
                else:
                    directions.append(f"Exit room {start_node.no_room} ({start_node.details})")
            except AttributeError:
                directions.append(f"Exit room {start_node.no_room}")

        changing_floor = False

        for i in range(1, len(path) - 1):
            current_node = self.info[path[i]]
            next_node = self.info[path[i + 1]]
            prev_node = self.info[path[i - 1]]
            
            if current_node.node_type == prev_node.node_type == next_node.node_type == 'h':
                continue
                
            if current_node.node_type == "he" and not changing_floor:
                changing_floor = True
                continue

            if changing_floor and current_node.node_type == "he" and next_node.node_type == "h":
                changing_floor = False
                floor_difference = current_node.floor - prev_node.floor
                directions.append(f"Go {floor_directions[floor_difference]} the stairs to {floor_mapping[current_node.floor]} floor")
            
            if changing_floor:
                continue

            steer_sign = self.__orientation_test(prev_node, current_node, next_node)
            steer_direction = steer_mapping[steer_sign]
            if steer_sign == 0 and current_node.node_type == 'h' and next_node.node_type == 's':
                directions.append(f'Your destination is straight ahead')
            elif steer_sign == 0 and current_node.node_type == 'h' and next_node.node_type == 'he':
                directions.append(f'Go to the stairs in front of you')
            elif current_node.node_type == 'h' and prev_node.node_type != 'h':
                directions.append(f"Go{' to the ' if steer_direction in ['right', 'left'] else ' '}{steer_direction}")
            elif current_node.node_type == 'h' and next_node.node_type != 'h':
                if next_node.node_type == 's':
                    directions.append(f"Your destination will be on the {steer_direction} side")
                else:
                    directions.append(f"Go to the {next_node.details} on the {steer_direction} side")
        
        return directions


    def __orientation_test(self, p, q, r):
        result = q.x * r.y + p.x * q.y + p.y * r.x - q.x * p.y - r.x * q.y - r.y * p.x
        return -1 if result < 0 else (1 if result > 0 else 0)


    def get_directions(self, start, finish):
        path = self.find_min_path(start, finish)
        return self.get_directions_for_path(path)
    
    def get_rooms_info(self):
        return [node_info for node_info in self.info.values() if node_info.node_type == 's']
    
    


