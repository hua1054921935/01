class TopoConfig:
    first_core_matric = 2000  # 第一个核心矩阵
    first_core_matric_new = 800  # 新的第一个核心矩阵
    level_gap = 600  # 水平差
    inner_level_gap = 100  # 内水平差距
    inner_leaf_gap = 100  # 内水平差距
    inner_level_gaps = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    def __init__(self, config):
        self.dic_indicator = {}
        self.dic_node_scale = {}
        self.dic_node_link = {}
        self.dic_node_link_bak = {}
        self.dic_type_node = {}
        self.dic_type = {}
        self.device = []
        self.processed_node = set()
        self.prepare_to_handle = []
        self.dic_node_position = {}

        self.first_core_center_pos = [0, 8000, 0]
        self.config = config
        self.min_position = [10000, 10000, 10000]
        self.max_position = [-10000, -10000, -10000]
        self.level_max = 0

    # 分析xml
    def analyse_xml(self):
        # content = base64.decodestring(self.config)
        content = self.config
        root = ET.fromstring(content)
        num = 0
        for i in root:
            if i.tag == 'node':
                num += 1
                link = []
                node = []
                node_id = i.attrib['id']
                type = i[0].attrib["uid"]
                self.dic_indicator[type] = 1
                link.append(type)
                self.dic_type_node[type] = node
                self.dic_node_link[node_id] = link
                self.dic_node_link_bak[node_id] = link
                self.dic_type[node_id] = type
            elif i.tag == 'link':
                t_id = i.attrib['target']
                s_id = i.attrib['source']
                self.dic_node_link[t_id].append(s_id)
                self.dic_node_link[s_id].append(t_id)
                self.dic_node_link_bak[t_id].append(s_id)
                self.dic_node_link_bak[s_id].append(t_id)

        if num > 10000:
            self.inner_level_gaps = [1, 11, 2.2, 0.5, 0.1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        elif num > 1000:
            self.inner_level_gaps = [1, 10, 8, 6, 8, 4, 8, 4, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        elif num > 500:
            self.inner_leaf_gap = 120
            self.inner_level_gaps = [1, 10, 8, 6, 8, 4, 8, 4, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        elif num > 100:
            self.inner_leaf_gap = 160
            self.inner_level_gaps = [1, 9, 4.2, 1, 0.1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        elif num > 50:
            self.inner_leaf_gap = 250
            self.inner_level_gaps = [1, 9, 4.2, 1, 0.1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        elif num > 10:
            self.inner_leaf_gap = 360
            self.inner_level_gaps = [1, 9, 4.2, 1, 0.1, 4, 8, 4, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        else:
            self.inner_leaf_gap = 400
            self.inner_level_gaps = [1, 9, 4.2, 1, 0.1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        # logger.debug(self.dic_node_link)
        for i in self.dic_node_link.iteritems():
            if self.dic_type_node.has_key(i[1][0]):
                self.dic_type_node[i[1][0]].append(i[0])
        # logger.debug(self.dic_type_node)
        for i in self.dic_indicator.iteritems():
            self.device.append(i[0])
        # logger.debug(self.device)
        return

    # 到下一级
    def get_next_level(self):
        # logger.debug(self.dic_indicator)
        if self.dic_indicator.has_key("router") and self.dic_indicator["router"]:
            return "router"
        elif self.dic_indicator.has_key("multi_switch") and self.dic_indicator["multi_switch"]:
            return "multi_switch"
        elif self.dic_indicator.has_key("firewall") and self.dic_indicator["firewall"]:
            return "firewall"
        elif self.dic_indicator.has_key("host") and self.dic_indicator["host"]:
            return "host"
        elif self.dic_indicator.has_key("server") and self.dic_indicator["server"]:
            return "server"
        elif self.dic_indicator.has_key("ids") and self.dic_indicator["ids"]:
            return "ids"
        elif self.dic_indicator.has_key("ips") and self.dic_indicator["ips"]:
            return "ips"
        else:
            return "done"

    # 刷新
    def refresh(self, allocate_node, level):
        self.processed_node = self.processed_node | set(allocate_node)
        if level:
            for node in allocate_node:
                node_level = [node, level]
                self.prepare_to_handle.append(node_level)
        return

    # 主要计算
    def main_calculate(self):

        type = self.get_next_level()
        if type == "done":
            return
        first_level_node = self.dic_type_node[type]
        self.dic_indicator[type] = 0
        first_core = []
        for i in iter(first_level_node):
            link = self.dic_node_link[i]
            link.pop(0)
            s = set(link)
            b = set(first_level_node)
            if s | b == b:
                first_core.append(i)
        s1 = set(first_level_node)
        s2 = set(first_core)
        first_other = list(s1 - s2)
        if first_core:
            self.allocate_position(first_core, 0, "")
            self.allocate_position(first_other, 1, self.first_core_center_pos)
        elif first_other:
            self.allocate_position(first_other, 1, self.first_core_center_pos)
        while (self.prepare_to_handle):
            p_node = self.prepare_to_handle.pop(0)
            link = self.dic_node_link[p_node[0]]
            link.pop(0)
            link = list(set(link) - (set(link) & self.processed_node))
            level = p_node[1] + 1
            pos = copy.deepcopy(self.dic_node_position[p_node[0]])
            pos[1] = pos[1] - self.level_gap
            self.allocate_position(link, level, pos)

    # 找到第一个
    def first_random_alocate(self, allocate_node):

        def get_pos():
            matrix = []
            core_pos_x = (random.choice(xrange(self.first_core_center_pos[0] - self.first_core_matric_new,
                                               self.first_core_center_pos[0] + self.first_core_matric_new)))
            core_pos_y = (random.choice(
                xrange(self.first_core_center_pos[1] - self.first_core_matric_new, self.first_core_center_pos[1])))
            core_pos_z = (random.choice(xrange(self.first_core_center_pos[2] - self.first_core_matric_new,
                                               self.first_core_center_pos[2] + self.first_core_matric_new)))

            matrix.append(core_pos_x)
            matrix.append(core_pos_y)
            matrix.append(core_pos_z)
            return matrix

        for i in range(len(allocate_node)):
            self.dic_node_position[allocate_node[i]] = get_pos()

        self.refresh(allocate_node, 0)

    # 循环分配
    def circle_allocate(self, allocate_node, level, center):
        if self.level_max < level:
            self.level_max = level
        self.refresh(allocate_node, level)
        locate_y = center[1] - 200
        locate_x = center[0]
        locate_z = center[2]
        if level == 1:
            locate_y = locate_y - 800
        if center[0] > 0:
            locate_x = center[0] + 200
        elif center[0] < 0:
            locate_x = center[0] - 200
        if center[2] > 0:
            locate_z = center[2] + 200
        elif center[2] < 0:
            locate_z = center[2] - 200
        r = self.first_core_matric / level
        part = len(allocate_node)

        if level == 1 and part > 8:
            self.refresh(allocate_node, level)
            tmp = int(math.ceil(math.sqrt(part)))
            mn = []
            k = (tmp - 1) / 2.0
            for m in range(tmp):
                for n in range(tmp):
                    mn.append([m - k, n - k])

            def comp(xx, yy):
                y = xx[0] * xx[0] + xx[1] * xx[1]
                x = yy[0] * yy[0] + yy[1] * yy[1]
                if x < y:
                    return 1
                elif x > y:
                    return -1
                else:
                    return 0

            mn.sort(comp)
            for i in range(part):
                if allocate_node:
                    ii = allocate_node.pop(0)
                    pos = []
                    if self.dic_type[ii] == 'host' or self.dic_type[ii] == 'server':
                        pos.append(locate_x + self.inner_leaf_gap * (mn[i][0]))
                        pos.append(locate_y)
                        pos.append(locate_z + self.inner_leaf_gap * (mn[i][1]))
                    else:
                        pos.append(locate_x + self.inner_level_gap * (mn[i][0]) * self.inner_level_gaps[level])
                        pos.append(locate_y)
                        pos.append(locate_z + self.inner_level_gap * (mn[i][1]) * self.inner_level_gaps[level])
                    self.dic_node_position[ii] = pos
            return

        for i in range(part):  # one position has already allocated
            if len(allocate_node):
                ii = allocate_node.pop(0)
            pos = []
            rr = r
            if self.dic_type[ii] == 'host' or self.dic_type[ii] == 'server':
                rr = self.inner_leaf_gap
            if level == 1:
                if i % 2:
                    x = locate_x + rr * 0.7 * round(math.cos(math.pi / part * 2 * i), 2)
                    z = locate_z + rr * 0.7 * round(math.sin(math.pi / part * 2 * i), 2)
                else:
                    x = locate_x + rr * round(math.cos(math.pi / part * 2 * i), 2)
                    z = locate_z + rr * round(math.sin(math.pi / part * 2 * i), 2)
            elif level != 1:
                x = locate_x + rr * round(math.cos(math.pi / part * 2 * i), 2)
                z = locate_z + rr * round(math.sin(math.pi / part * 2 * i), 2)

            pos.append(x), pos.append(locate_y), pos.append(z)
            self.dic_node_position[ii] = pos
        return

    # 原分配
    def raw_allocate(self, allocate_node, level, center):
        if self.level_max < level:
            self.level_max = level
        node_num = len(allocate_node)
        if node_num <= 64:
            self.refresh(allocate_node, level)
            tmp = int(math.ceil(math.sqrt(node_num)))
            mn = []
            k = (tmp - 1) / 2.0
            for m in range(tmp):
                for n in range(tmp):
                    mn.append([m - k, n - k])

            def comp(xx, yy):
                y = xx[0] * xx[0] + xx[1] * xx[1]
                x = yy[0] * yy[0] + yy[1] * yy[1]
                if x < y:
                    return 1
                elif x > y:
                    return -1
                else:
                    return 0

            mn.sort(comp)
            for i in range(node_num):
                if allocate_node:
                    ii = allocate_node.pop(0)
                    pos = []
                    if self.dic_type[ii] == 'host' or self.dic_type[ii] == 'server':
                        pos.append(center[0] + self.inner_leaf_gap * (mn[i][0]))
                        pos.append(center[1])
                        pos.append(center[2] + self.inner_leaf_gap * (mn[i][1]))
                    else:
                        pos.append(center[0] + self.inner_level_gap * (mn[i][0]) * self.inner_level_gaps[level])
                        pos.append(center[1])
                        pos.append(center[2] + self.inner_level_gap * (mn[i][1]) * self.inner_level_gaps[level])
                    self.dic_node_position[ii] = pos
        else:
            inner_center = center
            for i in range(len(allocate_node) / 64):
                for j in range(64):
                    subset = []
                    subset.append(allocate_node.pop(0))
                    self.raw_allocate(subset, level, inner_center)
                inner_center[1] = inner_center[1] - self.inner_level_gap * i
            if (len(allocate_node)):
                self.raw_allocate(allocate_node, level, inner_center)
        return

    # 分配位置
    def allocate_position(self, allocate_node, level, center):
        if self.level_max < level:
            self.level_max = level
        if level == 0:
            self.first_random_alocate(allocate_node)
        elif level == 1:
            self.circle_allocate(allocate_node, level, center)
        else:
            if len(allocate_node) <= 8 and len(allocate_node) > 0:
                self.circle_allocate(allocate_node, level, center)
            elif len(allocate_node) > 8:
                self.raw_allocate(allocate_node, level, center)
            else:
                return
        return

    # 中间点
    def cal_middle_point(self, point):
        self.min_position[0] = point[0] if point[0] < self.min_position[0] else self.min_position[0]
        self.min_position[1] = point[1] if point[1] < self.min_position[1] else self.min_position[1]
        self.min_position[2] = point[2] if point[2] < self.min_position[2] else self.min_position[2]

        self.max_position[0] = point[0] if point[0] > self.max_position[0] else self.max_position[0]
        self.max_position[1] = point[1] if point[1] > self.max_position[1] else self.max_position[1]
        self.max_position[2] = point[2] if point[2] > self.max_position[2] else self.max_position[2]

    # 最后的结果
    def final_result(self):
        setoff = 1
        if self.level_max > 6:
            setoff = 6.0 / self.level_max
        result = []

        for node in self.dic_node_position.iteritems():
            info = []
            info.append(node[0])
            info.append(self.dic_type[node[0]])
            for p in self.dic_node_position[node[0]]:
                info.append(p)
                pos = self.dic_node_position[node[0]]
                self.cal_middle_point(pos)
            info.append(0.9)
            info.append('whenlove')
            info.append('lvmy')
            info.append(3802)
            info.append(self.dic_node_link_bak[node[0]])
            info.append('')
            info.append('')
            info.append('')
            info[3] = int(info[3] * setoff)
            result.append(info)
        base64_result = base64.encodestring(str(result))

        result_dic = {'middlePoint': [], 'server': [], 'host': [], 'router': [], 'switch': [], 'ids': [], 'ips': [], 'firewall': []}
        result_dic['middlePoint'] = [0, 0, 0]
        for node in result:
            if node[1] == "server":
                result_dic['server'].append(node)
            elif node[1] == "host":
                result_dic['host'].append(node)
            elif node[1] == "router":
                result_dic['router'].append(node)
            elif node[1] == "multi_switch":
                result_dic['switch'].append(node)
            elif node[1] == "ids":
                result_dic['ids'].append(node)
            elif node[1] == "ips":
                result_dic['ips'].append(node)
            elif node[1] == "firewall":
                result_dic['firewall'].append(node)
        # result_dic['solarSystems'] = result
        '''
            result_dic['solarSystems'] = result
            response = HttpResponse(json.dumps(result_dic))
            response['Access-Control-Allow-Origin'] = '*'
            return response
        '''
        return result_dic

    def final_result_solar(self):
        result = []

        for node in self.dic_node_position.iteritems():
            info = []
            info.append(node[0])
            info.append(self.dic_type[node[0]])
            for p in self.dic_node_position[node[0]]:
                info.append(p)
                pos = self.dic_node_position[node[0]]
                self.cal_middle_point(pos)
            info.append(0.9)
            info.append('whenlove')
            info.append('lvmy')
            info.append(3802)
            info.append(self.dic_node_link_bak[node[0]])
            info.append('')
            info.append('')
            info.append('')
            result.append(info)
        base64_result = base64.encodestring(str(result))

        result_dic = {'middlePoint': [], 'server': [], 'host': [], 'router': [], 'switch': [], 'ids': [], 'ips': [], 'firewall': []}
        result_dic['middlePoint'] = [(self.min_position[0] + self.max_position[0]) * 0.5, (self.min_position[1] + self.max_position[1]) * 0.5, (self.min_position[2] + self.max_position[2]) * 0.5]
        for node in result:
            if node[1] == "server":
                result_dic['server'].append(node)
            elif node[1] == "host":
                result_dic['host'].append(node)
            elif node[1] == "router":
                result_dic['router'].append(node)
            elif node[1] == "multi_switch":
                result_dic['switch'].append(node)
            elif node[1] == "ids":
                result_dic['ids'].append(node)
            elif node[1] == "ips":
                result_dic['ips'].append(node)
            elif node[1] == "firewall":
                result_dic['firewall'].append(node)
        result_dic['solarSystems'] = result
        '''
            result_dic['solarSystems'] = result
            response = HttpResponse(json.dumps(result_dic))
            response['Access-Control-Allow-Origin'] = '*'
            return response
        '''
        return result_dic

    # 最终结果的位置
    def final_result_location(self):
        result = []
        for node in self.dic_node_position.iteritems():
            info = []
            info.append(node[0])
            info.append(self.dic_type[node[0]])
            for p in self.dic_node_position[node[0]]:
                info.append(p)
                pos = self.dic_node_position[node[0]]
                self.cal_middle_point(pos)
            info.append(0.9)
            info.append('whenlove')
            info.append('lvmy')
            info.append(3802)
            info.append(self.dic_node_link_bak[node[0]])
            # info.append('')
            # info.append('')
            # info.append('')
            result.append(info)
        base64_result = base64.encodestring(str(result))

        result_dic = {'middlePoint': [], 'server': [], 'host': [], 'router': [], 'switch': [], 'ids': [], 'ips': [], 'firewall': []}
        result_dic['middlePoint'] = [(self.min_position[0] + self.max_position[0]) * 0.5, (self.min_position[1] + self.max_position[1]) * 0.5, (self.min_position[2] + self.max_position[2]) * 0.5]
        self.location_compute(result)

        for node in result:
            if node[1] == "server":
                result_dic['server'].append(node)
            elif node[1] == "host":
                result_dic['host'].append(node)
            elif node[1] == "router":
                result_dic['router'].append(node)
            elif node[1] == "multi_switch":
                result_dic['switch'].append(node)
            elif node[1] == "ids":
                result_dic['ids'].append(node)
            elif node[1] == "ips":
                result_dic['ips'].append(node)
            elif node[1] == "firewall":
                result_dic['firewall'].append(node)

        result_dic['solarSystems'] = result
        response = HttpResponse(json.dumps(result_dic))
        response['Access-Control-Allow-Origin'] = '*'
        return response

    # 位置计算
    def location_compute(self, nodes):

        d = {}
        py = self.location
        pi = []
        index = 0
        h = sys.maxint
        for node in nodes:
            # node[2] -= point[0]
            node[3] -= self.first_core_matric
            # node[4] -= point[2]
            d[node[0]] = node
            if node[1] == "server" or node[1] == "host":
                pi.append(index)
                index += 1

        for node in nodes:
            if node[1] == "server" or node[1] == "host":
                pd = int(random.random() * len(pi))
                p = py[pi[pd]]
                del pi[pd]
                node.append(p['coordinate'][1])
                node.append(p['coordinate'][0])
                node.append('1')
                node.append(p['name'])
            else:
                node.append(0)
                node.append(0)
                node.append('0')
                node.append('')

            if h > node[3]:
                h = node[3]

        level = [0, 1, 2, 3, 4, 5, 6]
        for l in level:
            if l == 0:
                h += self.first_core_matric_new
            else:
                h += self.level_gap
            for node in nodes:
                if node[3] == h:
                    x = 0
                    y = 0
                    s = []
                    for i in node[9]:
                        if d[i][12] == '1' and i not in s:
                            s.append(i)
                            x += d[i][10]
                            y += d[i][11]
                    if len(s) > 0:
                        node[10] = x / len(s)
                        node[11] = y / len(s)

                    node[12] = '1'

        for node in nodes:
            if node[1] == "server" or node[1] == "host":
                node[12] = '1'
            else:
                node[12] = '0'
            if node[1] == "multi_switch":
                node[3] += 400
            elif node[1] == "router":
                node[3] += 800

    # 最终结果组
    def final_result_group(self):
        result = []
        for node in self.dic_node_position.iteritems():
            info = []
            info.append(node[0])
            info.append(self.dic_type[node[0]])
            for p in self.dic_node_position[node[0]]:
                info.append(p)
                pos = self.dic_node_position[node[0]]
                self.cal_middle_point(pos)
            info.append(0.9)
            info.append('whenlove')
            info.append('lvmy')
            info.append(3802)
            info.append(self.dic_node_link_bak[node[0]])
            # info.append('')
            # info.append('')
            # info.append('')
            result.append(info)
        base64_result = base64.encodestring(str(result))

        result_dic = {'middlePoint': [], 'server': [], 'host': [], 'router': [], 'switch': [], 'ids': [], 'ips': [], 'firewall': []}
        result_dic['middlePoint'] = [(self.min_position[0] + self.max_position[0]) * 0.5, (self.min_position[1] + self.max_position[1]) * 0.5, (self.min_position[2] + self.max_position[2]) * 0.5]

        self.location_compute_group(result)

        for node in result:
            if node[1] == "server":
                result_dic['server'].append(node)
            elif node[1] == "host":
                result_dic['host'].append(node)
            elif node[1] == "router":
                result_dic['router'].append(node)
            elif node[1] == "multi_switch":
                result_dic['switch'].append(node)
            elif node[1] == "ids":
                result_dic['ids'].append(node)
            elif node[1] == "ips":
                result_dic['ips'].append(node)
            elif node[1] == "firewall":
                result_dic['firewall'].append(node)

        result_dic['solarSystems'] = result
        response = HttpResponse(json.dumps(result_dic))
        response['Access-Control-Allow-Origin'] = '*'
        return response

    # 距离
    def distance(self, x1, x2, y1, y2, ):
        return (x1 - x2) ** 2 + (y1 - y2) ** 2

    # 位置计算组
    def location_compute_group(self, nodes):

        d = {}
        h = sys.maxint
        dp = {}
        py = self.location_group
        pi = []
        index = 0
        for node in nodes:
            # node[2] -= point[0]
            node[3] -= self.first_core_matric
            # node[4] -= point[2]
            d[node[0]] = node
            if node[1] == "server" or node[1] == "host":
                pi.append(index)
                index += 1

        for node in nodes:
            if node[1] == "server" or node[1] == "host":
                if len(node) < 12:
                    k = node[9][0]
                    if dp.has_key(k):
                        dist = sys.maxint
                        ii = 0
                        for i in pi:
                            point = py[i]
                            dd = self.distance(point['coordinate'][1], dp[k]['coordinate'][1], point['coordinate'][0],
                                               dp[k]['coordinate'][0])
                            if dd < dist:
                                dist = dd
                                p = point
                                pd = ii
                            ii += 1
                        del pi[pd]
                        dp[k]['coordinate'][1] = (dp[k]['coordinate'][1] + p['coordinate'][1]) * 0.5
                        dp[k]['coordinate'][0] = (dp[k]['coordinate'][0] + p['coordinate'][0]) * 0.5
                    else:
                        pd = 0
                        p = py[pi[pd]]
                        del pi[pd]
                        dp[k] = p

                    node.append(p['coordinate'][1])
                    node.append(p['coordinate'][0])
                    node.append('1')
                    node.append(p['name'])

                    for r in nodes:
                        if r[1] == "server" or r[1] == "host":
                            if len(r) < 12:
                                if r[9][0] == k:
                                    dist = sys.maxint
                                    ii = 0
                                    for i in pi:
                                        point = py[i]
                                        dd = self.distance(point['coordinate'][1], dp[k]['coordinate'][1],
                                                           point['coordinate'][0], dp[k]['coordinate'][0])
                                        if dd < dist:
                                            dist = dd
                                            p = point
                                            pd = ii
                                        ii += 1
                                    del pi[pd]
                                    dp[k]['coordinate'][1] = (dp[k]['coordinate'][1] + p['coordinate'][1]) * 0.5
                                    dp[k]['coordinate'][0] = (dp[k]['coordinate'][0] + p['coordinate'][0]) * 0.5

                                    r.append(p['coordinate'][1])
                                    r.append(p['coordinate'][0])
                                    r.append('1')
                                    r.append(p['name'])

                                    if h > r[3]:
                                        h = r[3]
            else:
                node.append(0)
                node.append(0)
                node.append('0')
                node.append('')

            if h > node[3]:
                h = node[3]

        level = [0, 1, 2, 3, 4, 5, 6]
        for l in level:
            if l == 0:
                h += self.first_core_matric_new
            else:
                h += self.level_gap
            for node in nodes:
                if node[3] == h:
                    x = 0
                    y = 0
                    s = []
                    for i in node[9]:
                        if d[i][12] == '1' and i not in s:
                            s.append(i)
                            x += d[i][10]
                            y += d[i][11]
                    if len(s) > 0:
                        node[10] = x / len(s)
                        node[11] = y / len(s)

                    node[12] = '1'

        for node in nodes:
            if node[1] == "server" or node[1] == "host":
                node[12] = '1'
            else:
                node[12] = '0'
            if node[1] == "multi_switch":
                node[3] += 100
            elif node[1] == "router":
                node[3] += 800
