def create_t_file(path, topo_data, view, node_dict):
    # return
    reload(sys)
    sys.setdefaultencoding('utf-8')

    content_xml = '<?xml version="1.0" encoding="utf-8"?><root><link_information> <delay>' + str(view['option'][
                                                                                                     'delay']) + '</delay><datarate>' + str(
        view['option']['datarate']) + '</datarate><mtu>' + str(view['option'][
                                                                   'mtu']) + '</mtu></link_information><id_range min="' + str(
        view['min']) + '" max="' + str(
        view['max']) + '"/><iptype><iptype>' + str(view['option']['iptype']) + '</iptype><ip netmask="' + \
                  view['option'][
                      'ipnetmask1'] + '" address="' + view['option']['ipaddress1'] + '"/><ip netmask="' + \
                  view['option']['ipnetmask2'] + '" address="' + view['option']['ipaddress2'] + '"/><ip netmask="' + \
                  view['option']['ipnetmask3'] + '" address="' + view['option']['ipaddress3'] + '"/></iptype>'
    node_category={'mms':"mms_",'sim':'sim_','emu':'emu_','rea':'rea_','con':'con_','open':'open_'}
    node_type={'r':"router",'s':'switch','h':'host','v':'server','d':'ids','p':'ips','f':'firewall'}
    for i in topo_data:
        node = node_dict[str(topo_data[i]['id'])]

        if node['node_category'] == 'mms':
            if node['node_type'] == 'r':
                content_xml += '<mms_router id="' + str(node['id']) + '" messagenum="' + str(
                    view['node_template']['messagenum']) + '" delay="' + str(view['node_template']['delay']) + '">'
                line = topo_data[i]['line']
                network = []
                flag = False
                xnt = 0
                nod = node
                if len(line) < 1:
                    if len(nod['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       str(view['option']['iptype']) + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype></interface>'
                for v in line:
                    # if topo_data[v]['id'] == nod['id']:
                    content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + node_category[topo_data[v]['node_category']]+node_type[topo_data[v]['node_type']] + '" >' + str(
                        topo_data[v]['id']) + '</link>'
                    if network:
                        f = False
                        for s in range(len(network)):
                            if network[s]['name'] == (sym['lines'][v]['dstSymbol'])[4:]:
                                content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                                               network[s]['ip'] + '" netmask="' + network[s][
                                                   'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                                               str(view['option']['iptype']) + '</iptype>'
                                f = True
                                break

                        if not f:
                            content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                           str(view['option']['iptype']) + '</iptype>'

                    else:
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'

                    # content_xml += '</interface>'
                    # flag = True
                    content_xml += '</interface>'
                    flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(line.index(v)) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</mms_router>'
            elif node['node_type'] == 's':
                content_xml += '<mms_switch id="' + str(node['id']) + '" messagenum="' + str(view['node_template'][
                                                                                                 'messagenum']) + '" delay="' + str(
                    view['node_template']['delay']) + '">'
                network = []
                line = topo_data[i]['line']
                flag = False
                xnt = 0
                nod = node
                if len(line) < 1:
                    if len(nod['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       str(view['option']['iptype']) + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in line:
                    # # if not sym['lines'][v].isExpand:
                    # if topo_data[v]['id'] == nod['id']:
                    xnt += 1
                    print get_symbol_type(topo_data[v]['id'])
                    content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + node_category[topo_data[v]['node_category']]+node_type[topo_data[v]['node_type']] + '" >' + str(
                        topo_data[v]['id']) + '</link>'
                    if network:
                        f = False
                        for s in range(len(network)):
                            if network[s]['name'] == (sym['lines'][v]['dstSymbol'])[4:]:
                                content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                                               network[s]['ip'] + '" netmask="' + network[s][
                                                   'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                                               str(view['option']['iptype']) + '</iptype>'
                                f = True
                                break

                        if not f:
                            content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                           str(view['option']['iptype']) + '</iptype>'
                    else:
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'

                    content_xml += '</interface>'
                    flag = True

                    # elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                    #     xnt += 1
                    #     content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + get_symbol_type(
                    #         sym['lines'][v]['srcSymbol']) + '" >' + str(
                    #         node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                    #     if network:
                    #         f = False
                    #         for s in range(len(network)):
                    #             if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
                    #                 content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                    #                     'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                    #                                network[s]['ip'] + '" netmask="' + network[s][
                    #                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                    #                                view['option']['iptype'] + '</iptype>'
                    #                 f = True
                    #                 break
                    #
                    #         if not f:
                    #             content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                    #                            view['option']['iptype'] + '</iptype>'
                    #
                    #     else:
                    #         content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                    #                        view['option']['iptype'] + '</iptype>'
                    #
                    #     content_xml += '</interface>'
                    #     flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(line.index(v)) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</mms_switch>'
            elif node['node_type'] == 'h':
                content_xml += '<mms_host id="' + str(node['id']) + '" messagenum="' + str(
                    view['node_template']['messagenum']) + '" delay="' + str(view['node_template']['delay']) + '">'
                network = []
                line = topo_data[i]['line']
                flag = False
                xnt = 0
                nod = node
                if len(line) < 1:
                    if len(nod['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in line:
                    # if not sym['lines'][v].isExpand:
                    # if topo_data[v]['id'] == nod['id']:
                    xnt += 1
                    content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + node_category[topo_data[v]['node_category']]+node_type[topo_data[v]['node_type']] + '" >' + str(
                        topo_data[v]['id']) + '</link>'
                    if network:
                        f = False
                        for s in range(len(network)):
                            if network[s]['name'] == (sym['lines'][v]['dstSymbol'])[4:]:
                                content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                                               network[s]['ip'] + '" netmask="' + network[s][
                                                   'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                                               view['option']['iptype'] + '</iptype>'
                                f = True
                                break

                        if not f:
                            content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                           view['option']['iptype'] + '</iptype>'

                    else:
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'

                    content_xml += '</interface>'
                    flag = True

                    # elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                    #     xnt += 1
                    #     content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + get_symbol_type(
                    #         sym['lines'][v]['srcSymbol']) + '" >' + str(
                    #         node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                    #     if network:
                    #         f = False
                    #         for s in range(len(network)):
                    #             if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
                    #                 content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                    #                     'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                    #                                network[s]['ip'] + '" netmask="' + network[s][
                    #                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                    #                                view['option']['iptype'] + '</iptype>'
                    #                 f = True
                    #                 break
                    #
                    #         if not f:
                    #             content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                    #                            view['option']['iptype'] + '</iptype>'
                    #
                    #     else:
                    #         content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                    #                        view['option']['iptype'] + '</iptype>'
                    #
                    #     content_xml += '</interface>'
                    #     flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(line.index(v)) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</mms_host>'
            elif node['node_type'] == 'v':

                content_xml += '<mms_server id="' + str(node['id']) + '" messagenum="' + str(
                    view['node_template']['messagenum']) + '" delay="' + str(view['node_template']['delay']) + '">'
                network = []
                line = topo_data[i]['line']
                flag = False
                xnt = 0
                nod = node
                if len(line) < 1:
                    if len(nod['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in line:
                    # if not sym['lines'][v].isExpand:
                    # if topo_data[v]['id'] == nod['id']:
                    xnt += 1
                    content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + node_category[topo_data[v]['node_category']]+node_type[topo_data[v]['node_type']] + '" >' + str(
                        topo_data[v]['id']) + '</link>'
                    if network:
                        f = False
                        for s in range(len(network)):
                            if network[s]['name'] == (sym['lines'][v]['dstSymbol'])[4:]:
                                content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                                               network[s]['ip'] + '" netmask="' + network[s][
                                                   'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                                               view['option']['iptype'] + '</iptype>'
                                f = True
                                break

                        if not f:
                            content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                           view['option']['iptype'] + '</iptype>'

                    else:
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'

                    content_xml += '</interface>'
                    flag = True

                    # elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                    #     xnt += 1
                    #     content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + get_symbol_type(
                    #         sym['lines'][v]['srcSymbol']) + '" >' + str(
                    #         node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                    #     if network:
                    #         f = False
                    #         for s in range(len(network)):
                    #             if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
                    #                 content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                    #                     'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                    #                                network[s]['ip'] + '" netmask="' + network[s][
                    #                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                    #                                view['option']['iptype'] + '</iptype>'
                    #                 f = True
                    #                 break
                    #
                    #         if not f:
                    #             content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                    #                            view['option']['iptype'] + '</iptype>'
                    #
                    #     else:
                    #         content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                    #                        view['option']['iptype'] + '</iptype>'
                    #
                    #     content_xml += '</interface>'
                    #     flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(line.index(v)) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</mms_server>'

        elif node['node_category'] == 'sim':
            if node['node_type'] == 'r':
                content_xml += '<router id="' + str(node['id']) + '" >'
                network = []
                flag = False
                xnt = 0
                nod = node
                if len(line) < 1:
                    if len(nod['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in line:
                    # if not sym['lines'][v].isExpand:
                    # if topo_data[v]['id'] == nod['id']:
                    xnt += 1
                    content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + node_category[topo_data[v]['node_category']]+node_type[topo_data[v]['node_type']] + '" >' + str(
                        topo_data[v]['id']) + '</link>'
                    if network:
                        f = False
                        for s in range(len(network)):
                            if network[s]['name'] == (sym['lines'][v]['dstSymbol'])[4:]:
                                content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                                               network[s]['ip'] + '" netmask="' + network[s][
                                                   'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                                               view['option']['iptype'] + '</iptype>'
                                f = True
                                break

                        if not f:
                            content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                           view['option']['iptype'] + '</iptype>'

                    else:
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'

                    content_xml += '</interface>'
                    flag = True

                    # elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                    #     xnt += 1
                    #     content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + get_symbol_type(
                    #         sym['lines'][v]['srcSymbol']) + '" >' + str(
                    #         node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                    #     if network:
                    #         f = False
                    #         for s in range(len(network)):
                    #             if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
                    #                 content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                    #                     'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                    #                                network[s]['ip'] + '" netmask="' + network[s][
                    #                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                    #                                str(view['option']['iptype']) + '</iptype>'
                    #                 f = True
                    #                 break
                    #
                    #         if not f:
                    #             content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                    #                            str(view['option']['iptype']) + '</iptype>'
                    #
                    #     else:
                    #         content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                    #                        str(view['option']['iptype']) + '</iptype>'
                    #
                    #     content_xml += '</interface>'
                    #     flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(line.index(v)) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</router>'
            elif node['node_type'] == 's':
                content_xml += '<switch id="' + str(node['id']) + '" >'
                network = []
                flag = False
                xnt = 0
                nod = node
                if len(line) < 1:
                    if len(nod['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       str(view['option']['iptype']) + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in line:
                    # if not sym['lines'][v].isExpand:
                    # if topo_data[v]['id'] == nod['id']:
                    xnt += 1
                    content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + node_category[topo_data[v]['node_category']]+node_type[topo_data[v]['node_type']] + '" >' + str(
                        topo_data[v]['id']) + '</link>'
                    if network:
                        f = False
                        for s in range(len(network)):
                            if network[s]['name'] == (sym['lines'][v]['dstSymbol'])[4:]:
                                content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                                               network[s]['ip'] + '" netmask="' + network[s][
                                                   'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                                               str(view['option']['iptype']) + '</iptype>'
                                f = True
                                break
                        if not f:
                            content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                           str(view['option']['iptype']) + '</iptype>'

                    else:
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'

                    content_xml += '</interface>'
                    flag = True

                    # elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                    #     xnt += 1
                    #     content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + get_symbol_type(
                    #         sym['lines'][v]['srcSymbol']) + '" >' + str(
                    #         node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                    #     if network:
                    #         f = False
                    #         for s in range(len(network)):
                    #             if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
                    #                 content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                    #                     'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                    #                                network[s]['ip'] + '" netmask="' + network[s][
                    #                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                    #                                str(view['option']['iptype']) + '</iptype>'
                    #                 f = True
                    #                 break
                    #
                    #         if not f:
                    #             content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                    #                            str(view['option']['iptype']) + '</iptype>'
                    #
                    #     else:
                    #         content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                    #                        str(view['option']['iptype']) + '</iptype>'
                    #
                    #     content_xml += '</interface>'
                    #     flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(line.index(v)) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</switch>'
            elif node['node_type'] == 'h':
                content_xml += '<host id="' + str(node['id']) + '" >'
                network = []
                flag = False
                xnt = 0
                nod = node
                if len(line) < 1:
                    if len(nod['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       str(view['option']['iptype']) + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in line:
                    # if not sym['lines'][v].isExpand:
                    # if topo_data[v]['id'] == nod['id']:
                    xnt += 1
                    content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + node_category[topo_data[v]['node_category']]+node_type[topo_data[v]['node_type']] + '" >' + str(
                        topo_data[v]['id']) + '</link>'
                    if network:
                        f = False
                        for s in range(len(network)):
                            if network[s]['name'] == (sym['lines'][v]['dstSymbol'])[4:]:
                                content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                                               network[s]['ip'] + '" netmask="' + network[s][
                                                   'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                                               str(view['option']['iptype']) + '</iptype>'
                                f = True
                                break

                        if not f:
                            content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                           str(view['option']['iptype']) + '</iptype>'

                    else:
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'

                    content_xml += '</interface>'
                    flag = True

                    # elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                    #     xnt += 1
                    #     content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + get_symbol_type(
                    #         sym['lines'][v]['srcSymbol']) + '" >' + str(
                    #         node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                    #     if network:
                    #         f = False
                    #         for s in range(len(network)):
                    #             if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
                    #                 content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                    #                     'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                    #                                network[s]['ip'] + '" netmask="' + network[s][
                    #                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                    #                                str(view['option']['iptype']) + '</iptype>'
                    #                 f = True
                    #                 break
                    #
                    #         if not f:
                    #             content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                    #                            str(view['option']['iptype']) + '</iptype>'
                    #
                    #     else:
                    #         content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                    #                        str(view['option']['iptype']) + '</iptype>'
                    #
                    #     content_xml += '</interface>'
                    #     flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(line.index(v)) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</host>'
            elif node['node_type'] == 'v':
                content_xml += '<server id="' + str(node['id']) + '" >'
                network = []
                flag = False
                xnt = 0
                nod = node
                if len(line) < 1:
                    if len(nod['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       str(view['option']['iptype']) + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in line:
                    # if not sym['lines'][v].isExpand:
                    # if topo_data[v]['id'] == nod['id']:
                    xnt += 1
                    content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + node_category[topo_data[v]['node_category']]+node_type[topo_data[v]['node_type']] + '" >' + str(
                        topo_data[v]['id']) + '</link>'
                    if network:
                        f = False
                        for s in range(len(network)):
                            if network[s]['name'] == (sym['lines'][v]['dstSymbol'])[4:]:
                                content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                                               network[s]['ip'] + '" netmask="' + network[s][
                                                   'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                                               str(view['option']['iptype']) + '</iptype>'
                                f = True
                                break

                        if not f:
                            content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                           str(view['option']['iptype']) + '</iptype>'

                    else:
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'

                    content_xml += '</interface>'
                    flag = True

                    # elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                    #     xnt += 1
                    #     content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + get_symbol_type(
                    #         sym['lines'][v]['srcSymbol']) + '" >' + str(
                    #         node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                    #     if network:
                    #         f = False
                    #         for s in range(len(network)):
                    #             if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
                    #                 content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                    #                     'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                    #                                network[s]['ip'] + '" netmask="' + network[s][
                    #                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                    #                                str(view['option']['iptype']) + '</iptype>'
                    #                 f = True
                    #                 break
                    #
                    #         if not f:
                    #             content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                    #                            str(view['option']['iptype']) + '</iptype>'
                    #
                    #     else:
                    #         content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                    #                        str(view['option']['iptype']) + '</iptype>'
                    #
                    #     content_xml += '</interface>'
                    #     flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(line.index(v)) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</server>'

        elif node['node_category'] == 'emu':
            if node['node_type'] == 'r':

                # if data[option['symbol_model']]:
                #     content_xml += '<real_router id="' + str(node['id']) + '" model="' + \
                #                    data[option['symbol_model']]['name'] + '">'
                # else:
                content_xml += '<real_router id="' + str(node['id']) + '" model="CISCO-7606S">'

                network = []
                flag = False
                xnt = 0
                nod = node
                if len(line) < 1:
                    if len(nod['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       str(view['option']['iptype']) + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in line:
                    # if not sym['lines'][v].isExpand:
                    # if topo_data[v]['id'] == nod['id']:
                    xnt += 1
                    content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + node_category[topo_data[v]['node_category']]+node_type[topo_data[v]['node_type']] + '" >' + str(
                        topo_data[v]['id']) + '</link>'
                    if network:
                        f = False
                        for s in range(len(network)):
                            if network[s]['name'] == (sym['lines'][v]['dstSymbol'])[4:]:
                                content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                                               network[s]['ip'] + '" netmask="' + network[s][
                                                   'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                                               str(view['option']['iptype']) + '</iptype>'
                                f = True
                                break

                        if not f:
                            content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                           str(view['option']['iptype']) + '</iptype>'

                    else:
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'

                    content_xml += '</interface>'
                    flag = True

                    # elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                    #     xnt += 1
                    #     content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + get_symbol_type(
                    #         sym['lines'][v]['srcSymbol']) + '" >' + str(
                    #         node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                    #     if network:
                    #         f = False
                    #         for s in range(len(network)):
                    #             if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
                    #                 content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                    #                     'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                    #                                network[s]['ip'] + '" netmask="' + network[s][
                    #                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                    #                                str(view['option']['iptype']) + '</iptype>'
                    #                 f = True
                    #                 break
                    #
                    #         if not f:
                    #             content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                    #                            str(view['option']['iptype']) + '</iptype>'
                    #
                    #     else:
                    #         content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                    #                        str(view['option']['iptype']) + '</iptype>'
                    #
                    #     content_xml += '</interface>'
                    #     flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(line.index(v)) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</real_router>'
            elif node['node_type'] == 's':

                content_xml += '<real_switch id="' + str(node['id']) + '" >'
                network = []
                flag = False
                xnt = 0
                nod = node
                if len(line) < 1:
                    if len(nod['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       str(view['option']['iptype']) + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in line:
                    # if not sym['lines'][v].isExpand:
                    # if topo_data[v]['id'] == nod['id']:
                    xnt += 1
                    content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + node_category[topo_data[v]['node_category']]+node_type[topo_data[v]['node_type']] + '" >' + str(
                        topo_data[v]['id']) + '</link>'
                    if network:
                        f = False
                        for s in range(len(network)):
                            if network[s]['name'] == (sym['lines'][v]['dstSymbol'])[4:]:
                                content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                                               network[s]['ip'] + '" netmask="' + network[s][
                                                   'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                                               str(view['option']['iptype']) + '</iptype>'
                                f = True
                                break

                        if not f:
                            content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                           str(view['option']['iptype']) + '</iptype>'

                    else:
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'

                    content_xml += '</interface>'
                    flag = True

                    # elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                    #     xnt += 1
                    #     content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + get_symbol_type(
                    #         sym['lines'][v]['srcSymbol']) + '" >' + str(
                    #         node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                    #     if network:
                    #         f = False
                    #         for s in range(len(network)):
                    #             if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
                    #                 content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                    #                     'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                    #                                network[s]['ip'] + '" netmask="' + network[s][
                    #                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                    #                                str(view['option']['iptype']) + '</iptype>'
                    #                 f = True
                    #                 break
                    #
                    #         if not f:
                    #             content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                    #                            str(view['option']['iptype']) + '</iptype>'
                    #
                    #     else:
                    #         content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                    #                        str(view['option']['iptype']) + '</iptype>'
                    #
                    #     content_xml += '</interface>'
                    #     flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(line.index(v)) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</real_switch>'
            elif node['node_type'] == 'h':

                content_xml += '<real_host id="' + str(node['id']) + '" >'
                # if data[option['symbol_cpumodel']]:
                #     content_xml += '<os><type arch="' + data[option['symbol_cpumodel']]['name'] + '" >' + \
                #                    data[option['operating_systemk']]['name'] + '</type></os>'
                # else:
                content_xml += '<os><type arch="i386" >windows</type></os>'

                network = []
                flag = False
                xnt = 0
                nod = node
                if len(line) < 1:
                    if len(nod['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       str(view['option']['iptype']) + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in line:
                    # if not sym['lines'][v].isExpand:
                    # if topo_data[v]['id'] == nod['id']:
                    xnt += 1
                    content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + node_category[topo_data[v]['node_category']]+node_type[topo_data[v]['node_type']] + '" >' + str(
                        topo_data[v]['id']) + '</link>'
                    if network:
                        f = False
                        for s in range(len(network)):
                            if network[s]['name'] == (sym['lines'][v]['dstSymbol'])[4:]:
                                content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                                               network[s]['ip'] + '" netmask="' + network[s][
                                                   'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                                               str(view['option']['iptype']) + '</iptype>'
                                f = True
                                break

                        if not f:
                            content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                           str(view['option']['iptype']) + '</iptype>'

                    else:
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'

                    content_xml += '</interface>'
                    flag = True

                    # elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                    #     xnt += 1
                    #     content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + get_symbol_type(
                    #         sym['lines'][v]['srcSymbol']) + '" >' + str(
                    #         node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                    #     if network:
                    #         f = False
                    #         for s in range(len(network)):
                    #             if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
                    #                 content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                    #                     'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                    #                                network[s]['ip'] + '" netmask="' + network[s][
                    #                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                    #                                str(view['option']['iptype']) + '</iptype>'
                    #                 f = True
                    #                 break
                    #
                    #         if not f:
                    #             content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                    #                            str(view['option']['iptype']) + '</iptype>'
                    #
                    #     else:
                    #         content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                    #                        str(view['option']['iptype']) + '</iptype>'
                    #
                    #     content_xml += '</interface>'
                    #     flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(line.index(v)) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</real_host>'
            elif node['node_type'] == 'v':

                content_xml += '<real_server id="' + str(node['id']) + '" >'
                # if data[option['symbol_cpumodel']]:
                #     content_xml += '<os><type arch="' + data[option['symbol_cpumodel']]['name'] + '" >' + \
                #                    data[option['operating_systemk']]['name'] + '</type></os>'
                # else:
                content_xml += '<os><type arch="i386" >windows</type></os>'

                network = []
                flag = False
                xnt = 0
                nod = node
                if len(line) < 1:
                    if len(nod['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       str(view['option']['iptype']) + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in line:
                    # if not sym['lines'][v].isExpand:
                    # if topo_data[v]['id'] == nod['id']:
                    xnt += 1
                    content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + node_category[topo_data[v]['node_category']]+node_type[topo_data[v]['node_type']] + '" >' + str(
                        topo_data[v]['id']) + '</link>'
                    if network:
                        f = False
                        for s in range(len(network)):
                            if network[s]['name'] == (sym['lines'][v]['dstSymbol'])[4:]:
                                content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                                               network[s]['ip'] + '" netmask="' + network[s][
                                                   'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                                               str(view['option']['iptype']) + '</iptype>'
                                f = True
                                break

                        if not f:
                            content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                           str(view['option']['iptype']) + '</iptype>'

                    else:
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'

                    content_xml += '</interface>'
                    flag = True

                    # elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                    #     xnt += 1
                    #     content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + get_symbol_type(
                    #         sym['lines'][v]['srcSymbol']) + '" >' + str(
                    #         node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                    #     if network:
                    #         f = False
                    #         for s in range(len(network)):
                    #             if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
                    #                 content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                    #                     'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                    #                                network[s]['ip'] + '" netmask="' + network[s][
                    #                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                    #                                str(view['option']['iptype']) + '</iptype>'
                    #                 f = True
                    #                 break
                    #
                    #         if not f:
                    #             content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                    #                            str(view['option']['iptype']) + '</iptype>'
                    #
                    #     else:
                    #         content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                    #                        str(view['option']['iptype']) + '</iptype>'
                    #
                    #     content_xml += '</interface>'
                    #     flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(line.index(v)) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</real_server>'
            elif node['node_type'] == 'd':

                content_xml += '<real_ids id="' + str(node['id']) + '" >'
                network = []
                flag = False
                xnt = 0
                nod = node
                if len(line) < 1:
                    if len(nod['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       str(view['option']['iptype']) + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in line:
                    # if sym['lines'][v].isExpand:
                    # if topo_data[v]['id'] == nod['id']:
                    xnt += 1
                    content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + node_category[topo_data[v]['node_category']]+node_type[topo_data[v]['node_type']] + '" >' + str(
                        topo_data[v]['id']) + '</link>'
                    if network:
                        f = False
                        for s in range(len(network)):
                            if network[s]['name'] == (sym['lines'][v]['dstSymbol'])[4:]:
                                content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                                               network[s]['ip'] + '" netmask="' + network[s][
                                                   'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                                               str(view['option']['iptype']) + '</iptype>'
                                content_xml += '<using_type>' + network[s]['port'] + '</using_type>'
                                f = True
                                break

                        if not f:
                            content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                           str(view['option']['iptype']) + '</iptype>'
                            content_xml += '<using_type>1</using_type>'

                    else:
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'
                        content_xml += '<using_type>1</using_type>'

                    content_xml += '</interface>'
                    flag = True

                    # elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                    #     xnt += 1
                    #     content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + get_symbol_type(
                    #         sym['lines'][v]['srcSymbol']) + '" >' + str(
                    #         node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                    #     if network:
                    #         f = False
                    #         for s in range(len(network)):
                    #             if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
                    #                 content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                    #                     'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                    #                                network[s]['ip'] + '" netmask="' + network[s][
                    #                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                    #                                str(view['option']['iptype']) + '</iptype>'
                    #                 content_xml += '<using_type>' + network[s]['port'] + '</using_type>'
                    #                 f = True
                    #                 break
                    #
                    #         if not f:
                    #             content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                    #                            str(view['option']['iptype']) + '</iptype>'
                    #             content_xml += '<using_type>1</using_type>'
                    #
                    #     else:
                    #         content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                    #                        str(view['option']['iptype']) + '</iptype>'
                    #         content_xml += '<using_type>1</using_type>'
                    #
                    #     content_xml += '</interface>'
                    #     flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(line.index(v)) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'
                        content_xml += '<using_type>1</using_type>'
                        content_xml += '</interface>'

                content_xml += '</real_ids>'
            elif node['node_type'] == 'p':

                content_xml += '<real_ips id="' + str(node['id']) + '" >'
                network = []
                flag = False
                xnt = 0
                nod = node
                if len(line) < 1:
                    if len(nod['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       str(view['option']['iptype']) + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in line:
                    # if not sym['lines'][v].isExpand:
                    # if topo_data[v]['id'] == nod['id']:
                    xnt += 1
                    content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + node_category[topo_data[v]['node_category']]+node_type[topo_data[v]['node_type']] + '" >' + str(
                        topo_data[v]['id']) + '</link>'
                    if network:
                        f = False
                        for s in range(len(network)):
                            if network[s]['name'] == (sym['lines'][v]['dstSymbol'])[4:]:
                                content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                                               network[s]['ip'] + '" netmask="' + network[s][
                                                   'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                                               str(view['option']['iptype']) + '</iptype>'
                                f = True
                                break

                        if not f:
                            content_xml += '<using_type>1</using_type>'

                    else:
                        content_xml += '<using_type>1</using_type>'

                    content_xml += '</interface>'
                    flag = True

                    # elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                    #     xnt += 1
                    #     content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + get_symbol_type(
                    #         sym['lines'][v]['srcSymbol']) + '" >' + str(
                    #         node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                    #     if network:
                    #         f = False
                    #         for s in range(len(network)):
                    #             if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
                    #                 content_xml += '<using_type>' + network[s]['port'] + '</using_type>'
                    #                 f = True
                    #                 break
                    #
                    #         if not f:
                    #             content_xml += '<using_type>1</using_type>'
                    #
                    #     else:
                    #         content_xml += '<using_type>1</using_type>'
                    #
                    #     content_xml += '</interface>'
                    #     flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(line.index(v)) + '">'
                        content_xml += '<using_type>1</using_type>'
                        content_xml += '</interface>'

                content_xml += '</real_ips>'
            elif node['node_type'] == 'f':

                content_xml += '<real_firewall id="' + str(node['id']) + '" >'
                network = []
                flag = False
                xnt = 0
                nod = node
                if len(line) < 1:
                    if len(nod['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       str(view['option']['iptype']) + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in line:
                    # if not sym['lines'][v].isExpand:
                    # if topo_data[v]['id'] == nod['id']:
                    xnt += 1
                    content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + node_category[topo_data[v]['node_category']]+node_type[topo_data[v]['node_type']] + '" >' + str(
                        topo_data[v]['id']) + '</link>'
                    if network:
                        f = False
                        for s in range(len(network)):
                            if network[s]['name'] == (sym['lines'][v]['dstSymbol'])[4:]:
                                content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                                               network[s]['ip'] + '" netmask="' + network[s][
                                                   'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                                               str(view['option']['iptype']) + '</iptype>'
                                content_xml += '<using_type>' + network[s]['port'] + '</using_type>'
                                f = True
                                break

                        if not f:
                            content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                           str(view['option']['iptype']) + '</iptype>'
                            content_xml += '<using_type>1</using_type>'

                    else:
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'
                        content_xml += '<using_type>1</using_type>'

                    content_xml += '</interface>'
                    flag = True

                    # elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                    #     xnt += 1
                    #     content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + get_symbol_type(
                    #         sym['lines'][v]['srcSymbol']) + '" >' + str(
                    #         node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                    #     if network:
                    #         f = False
                    #         for s in range(len(network)):
                    #             if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
                    #                 content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                    #                     'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                    #                                network[s]['ip'] + '" netmask="' + network[s][
                    #                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                    #                                str(view['option']['iptype']) + '</iptype>'
                    #                 content_xml += '<using_type>' + network[s]['port'] + '</using_type>'
                    #                 f = True
                    #                 break
                    #
                    #         if not f:
                    #             content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                    #                            str(view['option']['iptype']) + '</iptype>'
                    #             content_xml += '<using_type>1</using_type>'
                    #
                    #     else:
                    #         content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                    #                        str(view['option']['iptype']) + '</iptype>'
                    #         content_xml += '<using_type>1</using_type>'
                    #
                    #     content_xml += '</interface>'
                    #     flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(line.index(v)) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'
                        content_xml += '<using_type>1</using_type>'
                        content_xml += '</interface>'

                content_xml += '</real_firewall>'

        elif node['node_category'] == 'real':
            if node['node_type'] == 'r':
                content_xml += '<con_router id="' + str(node['id']) + '" messagenum="' + str(
                    view['node_template']['messagenum']) + '" delay="' + str(view['node_template']['delay']) + '">'
                network = []
                flag = False
                xnt = 0
                nod = node
                if len(line) < 1:
                    if len(nod['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       str(view['option']['iptype']) + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in line:
                    # if not sym['lines'][v].isExpand:
                    # if topo_data[v]['id'] == nod['id']:
                    xnt += 1
                    content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + node_category[topo_data[v]['node_category']]+node_type[topo_data[v]['node_type']] + '" >' + str(
                        topo_data[v]['id']) + '</link>'
                    if network:
                        f = False
                        for s in range(len(network)):
                            if network[s]['name'] == (sym['lines'][v]['dstSymbol'])[4:]:
                                content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                                               network[s]['ip'] + '" netmask="' + network[s][
                                                   'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                                               str(view['option']['iptype']) + '</iptype>'
                                f = True
                                break

                        if not f:
                            content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                           str(view['option']['iptype']) + '</iptype>'

                    else:
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'

                    content_xml += '</interface>'
                    flag = True

                    # elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                    #     xnt += 1
                    #     content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + get_symbol_type(
                    #         sym['lines'][v]['srcSymbol']) + '" >' + str(
                    #         node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                    #     if network:
                    #         f = False
                    #         for s in range(len(network)):
                    #             if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
                    #                 content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                    #                     'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                    #                                network[s]['ip'] + '" netmask="' + network[s][
                    #                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                    #                                str(view['option']['iptype']) + '</iptype>'
                    #                 f = True
                    #                 break
                    #
                    #         if not f:
                    #             content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                    #                            str(view['option']['iptype']) + '</iptype>'
                    #
                    #     else:
                    #         content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                    #                        str(view['option']['iptype']) + '</iptype>'
                    #
                    #     content_xml += '</interface>'
                    #     flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(line.index(v)) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</con_router>'
            elif node['node_type'] == 's':

                content_xml += '<con_switch id="' + str(node['id']) + '" messagenum="' + str(
                    view['node_template']['messagenum']) + '" delay="' + str(view['node_template']['delay']) + '">'
                network = []
                flag = False
                xnt = 0
                nod = node
                if len(line) < 1:
                    if len(nod['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       str(view['option']['iptype']) + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in line:
                    # if not sym['lines'][v].isExpand:
                    # if topo_data[v]['id'] == nod['id']:
                    xnt += 1
                    content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + node_category[topo_data[v]['node_category']]+node_type[topo_data[v]['node_type']] + '" >' + str(
                        topo_data[v]['id']) + '</link>'
                    if network:
                        f = False
                        for s in range(len(network)):
                            if network[s]['name'] == (sym['lines'][v]['dstSymbol'])[4:]:
                                content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                                               network[s]['ip'] + '" netmask="' + network[s][
                                                   'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                                               str(view['option']['iptype']) + '</iptype>'
                                f = True
                                break

                        if not f:
                            content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                           str(view['option']['iptype']) + '</iptype>'

                    else:
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'

                    content_xml += '</interface>'
                    flag = True

                    # elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                    #     xnt += 1
                    #     content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + get_symbol_type(
                    #         sym['lines'][v]['srcSymbol']) + '" >' + str(
                    #         node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                    #     if network:
                    #         f = False
                    #         for s in range(len(network)):
                    #             if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
                    #                 content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                    #                     'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                    #                                network[s]['ip'] + '" netmask="' + network[s][
                    #                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                    #                                str(view['option']['iptype']) + '</iptype>'
                    #                 f = True
                    #                 break
                    #
                    #         if not f:
                    #             content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                    #                            str(view['option']['iptype']) + '</iptype>'
                    #
                    #     else:
                    #         content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                    #                        str(view['option']['iptype']) + '</iptype>'
                    #
                    #     content_xml += '</interface>'
                    #     flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(line.index(v)) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</con_switch>'
            elif node['node_type'] == 'h':

                content_xml += '<con_host id="' + str(node['id']) + '" messagenum="' + str(
                    view['node_template']['messagenum']) + '" delay="' + str(view['node_template']['delay']) + '">'
                network = []
                flag = False
                xnt = 0
                nod = node
                if len(line) < 1:
                    if len(nod['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       str(view['option']['iptype']) + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in line:
                    # if not sym['lines'][v].isExpand:
                    # if topo_data[v]['id'] == nod['id']:
                    xnt += 1
                    content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + node_category[topo_data[v]['node_category']]+node_type[topo_data[v]['node_type']] + '" >' + str(
                        topo_data[v]['id']) + '</link>'
                    if network:
                        f = False
                        for s in range(len(network)):
                            if network[s]['name'] == (sym['lines'][v]['dstSymbol'])[4:]:
                                content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                                               network[s]['ip'] + '" netmask="' + network[s][
                                                   'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                                               str(view['option']['iptype']) + '</iptype>'
                                f = True
                                break

                        if not f:
                            content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                           str(view['option']['iptype']) + '</iptype>'

                    else:
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'

                    content_xml += '</interface>'
                    flag = True

                    # elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                    #     xnt += 1
                    #     content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + get_symbol_type(
                    #         sym['lines'][v]['srcSymbol']) + '" >' + str(
                    #         node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                    #     if network:
                    #         f = False
                    #         for s in range(len(network)):
                    #             if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
                    #                 content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                    #                     'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                    #                                network[s]['ip'] + '" netmask="' + network[s][
                    #                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                    #                                str(view['option']['iptype']) + '</iptype>'
                    #                 f = True
                    #                 break
                    #
                    #         if not f:
                    #             content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                    #                            str(view['option']['iptype']) + '</iptype>'
                    #
                    #     else:
                    #         content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                    #                        str(view['option']['iptype']) + '</iptype>'
                    #
                    #     content_xml += '</interface>'
                    #     flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(line.index(v)) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</con_host>'
            elif node['node_type'] == 'v':
                content_xml += '<con_server id="' + str(node['id']) + '" messagenum="' + str(
                    view['node_template']['messagenum']) + '" delay="' + str(view['node_template']['delay']) + '">'
                network = []
                flag = False
                xnt = 0
                nod = node
                if len(line) < 1:
                    if len(nod['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       str(view['option']['iptype']) + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in line:
                    # if not sym['lines'][v].isExpand:
                    # if topo_data[v]['id'] == nod['id']:
                    xnt += 1
                    content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + node_category[topo_data[v]['node_category']]+node_type[topo_data[v]['node_type']] + '" >' + str(
                        topo_data[v]['id']) + '</link>'
                    if network:
                        f = False
                        for s in range(len(network)):
                            if network[s]['name'] == (sym['lines'][v]['dstSymbol'])[4:]:
                                content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                                               network[s]['ip'] + '" netmask="' + network[s][
                                                   'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                                               str(view['option']['iptype']) + '</iptype>'
                                f = True
                                break

                        if not f:
                            content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                           str(view['option']['iptype']) + '</iptype>'

                    else:
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'

                    content_xml += '</interface>'
                    flag = True

                    # elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                    #     xnt += 1
                    #     content_xml += '<interface id="' + str(line.index(v)) + '"><link type="' + get_symbol_type(
                    #         sym['lines'][v]['srcSymbol']) + '" >' + str(
                    #         node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                    #     if network:
                    #         f = False
                    #         for s in range(len(network)):
                    #             if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
                    #                 content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                    #                     'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                    #                                network[s]['ip'] + '" netmask="' + network[s][
                    #                                    'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                    #                                str(view['option']['iptype']) + '</iptype>'
                    #                 f = True
                    #                 break
                    #
                    #         if not f:
                    #             content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                    #                            str(view['option']['iptype']) + '</iptype>'
                    #
                    #     else:
                    #         content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                    #                        str(view['option']['iptype']) + '</iptype>'
                    #
                    #     content_xml += '</interface>'
                    #     flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(line.index(v)) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       str(view['option']['iptype']) + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</con_server>'

    content_xml += '</root>'
    f = open(path, "wb")
    f.write(content_xml)
    f.close()

    return content_xml
dict1[order]={'site':[],'line':links,'node_type':node['node_type'],'node_category':node['node_category'],'id':node['id']}
