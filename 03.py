def create_t_file(path, topo_data,view,node_dict):
    reload(sys)
    sys.setdefaultencoding('utf-8')

    content_xml = '<?xml version="1.0" encoding="utf-8"?><root><link_information> <delay>' + view['option'][
        'delay'] + '</delay><datarate>' + view['option']['datarate'] + '</datarate><mtu>' + view['option'][
                      'mtu'] + '</mtu></link_information><id_range min="' + str(view['min']) + '" max="' + str(
        view['max']) + '"/><iptype><iptype>' + view['option']['iptype'] + '</iptype><ip netmask="' + view['option'][
                      'ipnetmask1'] + '" address="' + view['option']['ipaddress1'] + '"/><ip netmask="' + \
                  view['option']['ipnetmask2'] + '" address="' + view['option']['ipaddress2'] + '"/><ip netmask="' + \
                  view['option']['ipnetmask3'] + '" address="' + view['option']['ipaddress3'] + '"/></iptype>'
    for i in range(len(topo_data)):
        symbol = node_dict[i]

        if symbol['type'] == "1":
            continue

        def get_symbol_type(id):

            reload(sys)
            sys.setdefaultencoding('utf-8')

            for id_index in range(len(nodes)):
                if nodes[id_index]['id'] == id:
                    t = nodes[id_index]

            l_start = ""
            l_end = ""
            if t['option']['symbol_type'] == '40031':
                l_start = "mms_"
            elif t['option']['symbol_type'] == '40032':
                l_start = ""
            elif t['option']['symbol_type'] == '40033':
                l_start = "emu_"
            elif t['option']['symbol_type'] == '40034':
                l_start = "real_"
            elif t['option']['symbol_type'] == '40035':
                l_start = "con_"
            elif t['option']['symbol_type'] == '40036':
                l_start = "open_"

            if t['objectClass'] == '3001':
                return l_start + "router"
            elif t['objectClass'] == '3002':
                return l_start + "switch"
            elif t['objectClass'] == '3003':
                return l_start + "host"
            elif t['objectClass'] == '3004':
                return l_start + "server"
            elif t['objectClass'] == '3005':
                return l_start + "ids"
            elif t['objectClass'] == '3006':
                return l_start + "ips"
            elif t['objectClass'] == '3007':
                return l_start + "firewall"

        if symbol['option']['symbol_type'] == '40031':
            if symbol['objectClass'] == '3001':
                option = symbol['option']
                content_xml += '<mms_router id="' + str(symbol['uid']) + '" messagenum="' + str(
                    option['information']) + '" delay="' + str(option['delay']) + '">'
                network = symbol['net']
                flag = False
                xnt = 0
                sym = symbol
                if len(sym['lines']) < 1:
                    if len(sym['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                for v in sym['lines']:
                    if sym['lines'][v]['srcSymbol'] == sym['id']:
                        content_xml += '<interface id="' + v + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['dstSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                        content_xml += '<interface id="' + v + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['srcSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                        if network:
                            f = False
                            for s in range(len(network)):
                                if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       view['option']['iptype'] + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</mms_router>'
            elif symbol['objectClass'] == '3002':
                option = symbol['option']
                content_xml += '<mms_switch id="' + str(symbol['uid']) + '" messagenum="' + option[
                    'information'] + '" delay="' + str(option['delay']) + '">'
                network = symbol['net']
                flag = False
                xnt = 0
                sym = symbol
                if len(sym['lines']) < 1:
                    if len(sym['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in sym['lines']:
                    # # if not sym['lines'][v].isExpand:
                    if sym['lines'][v]['srcSymbol'] == sym['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['dstSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['srcSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                        if network:
                            f = False
                            for s in range(len(network)):
                                if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       view['option']['iptype'] + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</mms_switch>'
            elif symbol['objectClass'] == '3003':
                option = symbol['option']
                content_xml += '<mms_host id="' + str(symbol['uid']) + '" messagenum="' + option[
                    'information'] + '" delay="' + str(option['delay']) + '">'
                network = symbol['net']

                flag = False
                xnt = 0
                sym = symbol
                if len(sym['lines']) < 1:
                    if len(sym['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in sym['lines']:
                    # if not sym['lines'][v].isExpand:
                    if sym['lines'][v]['srcSymbol'] == sym['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['dstSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['srcSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                        if network:
                            f = False
                            for s in range(len(network)):
                                if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       view['option']['iptype'] + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</mms_host>'
            elif symbol['objectClass'] == '3004':
                option = symbol['option']
                content_xml += '<mms_server id="' + str(symbol['uid']) + '" messagenum="' + option[
                    'information'] + '" delay="' + str(option['delay']) + '">'
                network = symbol['net']
                flag = False
                xnt = 0
                sym = symbol
                if len(sym['lines']) < 1:
                    if len(sym['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in sym['lines']:
                    # if not sym['lines'][v].isExpand:
                    if sym['lines'][v]['srcSymbol'] == sym['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['dstSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['srcSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                        if network:
                            f = False
                            for s in range(len(network)):
                                if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       view['option']['iptype'] + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</mms_server>'

        elif symbol['option']['symbol_type'] == '40032':
            if symbol['objectClass'] == '3001':
                option = symbol['option']
                content_xml += '<router id="' + str(symbol['uid']) + '" >'
                network = symbol['net']
                flag = False
                xnt = 0
                sym = symbol
                if len(sym['lines']) < 1:
                    if len(sym['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in sym['lines']:
                    # if not sym['lines'][v].isExpand:
                    if sym['lines'][v]['srcSymbol'] == sym['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['dstSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['srcSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                        if network:
                            f = False
                            for s in range(len(network)):
                                if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       view['option']['iptype'] + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</router>'
            elif symbol['objectClass'] == '3002':
                option = symbol['option']
                content_xml += '<switch id="' + str(symbol['uid']) + '" >'
                network = symbol['net']
                flag = False
                xnt = 0
                sym = symbol
                if len(sym['lines']) < 1:
                    if len(sym['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in sym['lines']:
                    # if not sym['lines'][v].isExpand:
                    if sym['lines'][v]['srcSymbol'] == sym['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['dstSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['srcSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                        if network:
                            f = False
                            for s in range(len(network)):
                                if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       view['option']['iptype'] + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</switch>'
            elif symbol['objectClass'] == '3003':
                option = symbol['option']
                content_xml += '<host id="' + str(symbol['uid']) + '" >'
                network = symbol['net']
                flag = False
                xnt = 0
                sym = symbol
                if len(sym['lines']) < 1:
                    if len(sym['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in sym['lines']:
                    # if not sym['lines'][v].isExpand:
                    if sym['lines'][v]['srcSymbol'] == sym['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['dstSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['srcSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                        if network:
                            f = False
                            for s in range(len(network)):
                                if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       view['option']['iptype'] + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</host>'
            elif symbol['objectClass'] == '3004':
                option = symbol['option']
                content_xml += '<server id="' + str(symbol['uid']) + '" >'
                network = symbol['net']
                flag = False
                xnt = 0
                sym = symbol
                if len(sym['lines']) < 1:
                    if len(sym['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in sym['lines']:
                    # if not sym['lines'][v].isExpand:
                    if sym['lines'][v]['srcSymbol'] == sym['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['dstSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['srcSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                        if network:
                            f = False
                            for s in range(len(network)):
                                if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       view['option']['iptype'] + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</server>'

        elif symbol['option']['symbol_type'] == '40034':
            if symbol['objectClass'] == '3001':
                option = symbol['option']
                if data[option['symbol_model']]:
                    content_xml += '<real_router id="' + str(symbol['uid']) + '" model="' + \
                                   data[option['symbol_model']]['name'] + '">'
                else:
                    content_xml += '<real_router id="' + str(symbol['uid']) + '" model="CISCO-7606S">'

                network = symbol['net']
                flag = False
                xnt = 0
                sym = symbol
                if len(sym['lines']) < 1:
                    if len(sym['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in sym['lines']:
                    # if not sym['lines'][v].isExpand:
                    if sym['lines'][v]['srcSymbol'] == sym['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['dstSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['srcSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                        if network:
                            f = False
                            for s in range(len(network)):
                                if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       view['option']['iptype'] + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</real_router>'
            elif symbol['objectClass'] == '3002':
                option = symbol['option']
                content_xml += '<real_switch id="' + str(symbol['uid']) + '" >'
                network = symbol['net']
                flag = False
                xnt = 0
                sym = symbol
                if len(sym['lines']) < 1:
                    if len(sym['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in sym['lines']:
                    # if not sym['lines'][v].isExpand:
                    if sym['lines'][v]['srcSymbol'] == sym['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['dstSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['srcSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                        if network:
                            f = False
                            for s in range(len(network)):
                                if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       view['option']['iptype'] + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</real_switch>'
            elif symbol['objectClass'] == '3003':
                option = symbol['option']
                content_xml += '<real_host id="' + str(symbol['uid']) + '" >'
                if data[option['symbol_cpumodel']]:
                    content_xml += '<os><type arch="' + data[option['symbol_cpumodel']]['name'] + '" >' + \
                                   data[option['operating_systemk']]['name'] + '</type></os>'
                else:
                    content_xml += '<os><type arch="i386" >windows</type></os>'

                network = symbol['net']
                flag = False
                xnt = 0
                sym = symbol
                if len(sym['lines']) < 1:
                    if len(sym['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in sym['lines']:
                    # if not sym['lines'][v].isExpand:
                    if sym['lines'][v]['srcSymbol'] == sym['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['dstSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['srcSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                        if network:
                            f = False
                            for s in range(len(network)):
                                if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       view['option']['iptype'] + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</real_host>'
            elif symbol['objectClass'] == '3004':
                option = symbol['option']
                content_xml += '<real_server id="' + str(symbol['uid']) + '" >'
                if data[option['symbol_cpumodel']]:
                    content_xml += '<os><type arch="' + data[option['symbol_cpumodel']]['name'] + '" >' + \
                                   data[option['operating_systemk']]['name'] + '</type></os>'
                else:
                    content_xml += '<os><type arch="i386" >windows</type></os>'

                network = symbol['net']
                flag = False
                xnt = 0
                sym = symbol
                if len(sym['lines']) < 1:
                    if len(sym['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in sym['lines']:
                    # if not sym['lines'][v].isExpand:
                    if sym['lines'][v]['srcSymbol'] == sym['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['dstSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['srcSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                        if network:
                            f = False
                            for s in range(len(network)):
                                if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       view['option']['iptype'] + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</real_server>'
            elif symbol['objectClass'] == '3005':
                option = symbol['option']
                content_xml += '<real_ids id="' + str(symbol['uid']) + '" >'
                network = symbol['net']
                flag = False
                xnt = 0
                sym = symbol
                if len(sym['lines']) < 1:
                    if len(sym['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in sym['lines']:
                    # if sym['lines'][v].isExpand:
                    if sym['lines'][v]['srcSymbol'] == sym['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['dstSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'
                        if network:
                            f = False
                            for s in range(len(network)):
                                if network[s]['name'] == (sym['lines'][v]['dstSymbol'])[4:]:
                                    content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                                        'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                                                   network[s]['ip'] + '" netmask="' + network[s][
                                                       'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                                                   view['option']['iptype'] + '</iptype>'
                                    content_xml += '<using_type>' + network[s]['port'] + '</using_type>'
                                    f = True
                                    break

                            if not f:
                                content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                               view['option']['iptype'] + '</iptype>'
                                content_xml += '<using_type>1</using_type>'

                        else:
                            content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                           view['option']['iptype'] + '</iptype>'
                            content_xml += '<using_type>1</using_type>'

                        content_xml += '</interface>'
                        flag = True

                    elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['srcSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                        if network:
                            f = False
                            for s in range(len(network)):
                                if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
                                    content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                                        'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                                                   network[s]['ip'] + '" netmask="' + network[s][
                                                       'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                                                   view['option']['iptype'] + '</iptype>'
                                    content_xml += '<using_type>' + network[s]['port'] + '</using_type>'
                                    f = True
                                    break

                            if not f:
                                content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                               view['option']['iptype'] + '</iptype>'
                                content_xml += '<using_type>1</using_type>'

                        else:
                            content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                           view['option']['iptype'] + '</iptype>'
                            content_xml += '<using_type>1</using_type>'

                        content_xml += '</interface>'
                        flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       view['option']['iptype'] + '</iptype>'
                        content_xml += '<using_type>1</using_type>'
                        content_xml += '</interface>'

                content_xml += '</real_ids>'
            elif symbol['objectClass'] == '3006':
                option = symbol['option']
                content_xml += '<real_ips id="' + str(symbol['uid']) + '" >'
                network = symbol['net']
                flag = False
                xnt = 0
                sym = symbol
                if len(sym['lines']) < 1:
                    if len(sym['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in sym['lines']:
                    # if not sym['lines'][v].isExpand:
                    if sym['lines'][v]['srcSymbol'] == sym['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['dstSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'
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
                                content_xml += '<using_type>1</using_type>'

                        else:
                            content_xml += '<using_type>1</using_type>'

                        content_xml += '</interface>'
                        flag = True

                    elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['srcSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                        if network:
                            f = False
                            for s in range(len(network)):
                                if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
                                    content_xml += '<using_type>' + network[s]['port'] + '</using_type>'
                                    f = True
                                    break

                            if not f:
                                content_xml += '<using_type>1</using_type>'

                        else:
                            content_xml += '<using_type>1</using_type>'

                        content_xml += '</interface>'
                        flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '">'
                        content_xml += '<using_type>1</using_type>'
                        content_xml += '</interface>'

                content_xml += '</real_ips>'
            elif symbol['objectClass'] == '3007':
                option = symbol['option']
                content_xml += '<real_firewall id="' + str(symbol['uid']) + '" >'
                network = symbol['net']
                flag = False
                xnt = 0
                sym = symbol
                if len(sym['lines']) < 1:
                    if len(sym['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in sym['lines']:
                    # if not sym['lines'][v].isExpand:
                    if sym['lines'][v]['srcSymbol'] == sym['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['dstSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'
                        if network:
                            f = False
                            for s in range(len(network)):
                                if network[s]['name'] == (sym['lines'][v]['dstSymbol'])[4:]:
                                    content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                                        'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                                                   network[s]['ip'] + '" netmask="' + network[s][
                                                       'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                                                   view['option']['iptype'] + '</iptype>'
                                    content_xml += '<using_type>' + network[s]['port'] + '</using_type>'
                                    f = True
                                    break

                            if not f:
                                content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                               view['option']['iptype'] + '</iptype>'
                                content_xml += '<using_type>1</using_type>'

                        else:
                            content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                           view['option']['iptype'] + '</iptype>'
                            content_xml += '<using_type>1</using_type>'

                        content_xml += '</interface>'
                        flag = True

                    elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['srcSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                        if network:
                            f = False
                            for s in range(len(network)):
                                if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
                                    content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                                        'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><iptype address="' + \
                                                   network[s]['ip'] + '" netmask="' + network[s][
                                                       'subnetmask'] + '" gateway="' + network[s]['gateway'] + '">' + \
                                                   view['option']['iptype'] + '</iptype>'
                                    content_xml += '<using_type>' + network[s]['port'] + '</using_type>'
                                    f = True
                                    break

                            if not f:
                                content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                               view['option']['iptype'] + '</iptype>'
                                content_xml += '<using_type>1</using_type>'

                        else:
                            content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                           view['option']['iptype'] + '</iptype>'
                            content_xml += '<using_type>1</using_type>'

                        content_xml += '</interface>'
                        flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       view['option']['iptype'] + '</iptype>'
                        content_xml += '<using_type>1</using_type>'
                        content_xml += '</interface>'

                content_xml += '</real_firewall>'

        elif symbol['option']['symbol_type'] == '40035':
            if symbol['objectClass'] == '3001':
                option = symbol['option']
                content_xml += '<con_router id="' + str(symbol['uid']) + '" messagenum="' + option[
                    'information'] + '" delay="' + str(option['delay']) + '">'
                network = symbol['net']
                flag = False
                xnt = 0
                sym = symbol
                if len(sym['lines']) < 1:
                    if len(sym['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in sym['lines']:
                    # if not sym['lines'][v].isExpand:
                    if sym['lines'][v]['srcSymbol'] == sym['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['dstSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['srcSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                        if network:
                            f = False
                            for s in range(len(network)):
                                if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       view['option']['iptype'] + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</con_router>'
            elif symbol['objectClass'] == '3002':
                option = symbol['option']
                content_xml += '<con_switch id="' + str(symbol['uid']) + '" messagenum="' + option[
                    'information'] + '" delay="' + str(option['delay']) + '">'
                network = symbol['net']
                flag = False
                xnt = 0
                sym = symbol
                if len(sym['lines']) < 1:
                    if len(sym['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in sym['lines']:
                    # if not sym['lines'][v].isExpand:
                    if sym['lines'][v]['srcSymbol'] == sym['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['dstSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['srcSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                        if network:
                            f = False
                            for s in range(len(network)):
                                if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       view['option']['iptype'] + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</con_switch>'
            elif symbol['objectClass'] == '3003':
                option = symbol['option']
                content_xml += '<con_host id="' + str(symbol['uid']) + '" messagenum="' + option[
                    'information'] + '" delay="' + str(option['delay']) + '">'
                network = symbol['net']
                flag = False
                xnt = 0
                sym = symbol
                if len(sym['lines']) < 1:
                    if len(sym['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in sym['lines']:
                    # if not sym['lines'][v].isExpand:
                    if sym['lines'][v]['srcSymbol'] == sym['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['dstSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['srcSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                        if network:
                            f = False
                            for s in range(len(network)):
                                if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       view['option']['iptype'] + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</con_host>'
            elif symbol['objectClass'] == '3004':
                option = symbol['option']
                content_xml += '<con_server id="' + str(symbol['uid']) + '" messagenum="' + option[
                    'information'] + '" delay="' + str(option['delay']) + '">'
                network = symbol['net']
                flag = False
                xnt = 0
                sym = symbol
                if len(sym['lines']) < 1:
                    if len(sym['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in sym['lines']:
                    # if not sym['lines'][v].isExpand:
                    if sym['lines'][v]['srcSymbol'] == sym['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['dstSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['srcSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                        if network:
                            f = False
                            for s in range(len(network)):
                                if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       view['option']['iptype'] + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</con_server>'

        elif symbol['option']['symbol_type'] == '40036':
            if symbol['objectClass'] == '3001':
                option = symbol['option']
                content_xml += '<open_router id="' + str(symbol['uid']) + '" messagenum="' + option[
                    'information'] + '" delay="' + str(option['delay']) + '">'
                network = symbol['net']
                flag = False
                xnt = 0
                sym = symbol
                if len(sym['lines']) < 1:
                    if len(sym['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in sym['lines']:
                    # if not sym['lines'][v].isExpand:
                    if sym['lines'][v]['srcSymbol'] == sym['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['dstSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['srcSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                        if network:
                            f = False
                            for s in range(len(network)):
                                if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       view['option']['iptype'] + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</open_router>'
            elif symbol['objectClass'] == '3002':
                option = symbol['option']
                content_xml += '<open_switch id="' + str(symbol['uid']) + '" messagenum="' + option[
                    'information'] + '" delay="' + str(option['delay']) + '">'
                network = symbol['net']
                flag = False
                xnt = 0
                sym = symbol
                if len(sym['lines']) < 1:
                    if len(sym['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in sym['lines']:
                    # if not sym['lines'][v].isExpand:
                    if sym['lines'][v]['srcSymbol'] == sym['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['dstSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['srcSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                        if network:
                            f = False
                            for s in range(len(network)):
                                if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       view['option']['iptype'] + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</open_switch>'
            elif symbol['objectClass'] == '3003':
                option = symbol['option']
                content_xml += '<open_host id="' + str(symbol['uid']) + '" messagenum="' + option[
                    'information'] + '" delay="' + str(option['delay']) + '">'
                network = symbol['net']
                flag = False
                xnt = 0
                sym = symbol
                if len(sym['lines']) < 1:
                    if len(sym['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in sym['lines']:
                    # if not sym['lines'][v].isExpand:
                    if sym['lines'][v]['srcSymbol'] == sym['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['dstSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['srcSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                        if network:
                            f = False
                            for s in range(len(network)):
                                if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       view['option']['iptype'] + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</open_host>'
            elif symbol['objectClass'] == '3004':
                option = symbol['option']
                content_xml += '<open_server id="' + str(symbol['uid']) + '" messagenum="' + option[
                    'information'] + '" delay="' + str(option['delay']) + '">'
                network = symbol['net']
                flag = False
                xnt = 0
                sym = symbol
                if len(sym['lines']) < 1:
                    if len(sym['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in sym['lines']:
                    # if not sym['lines'][v].isExpand:
                    if sym['lines'][v]['srcSymbol'] == sym['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['dstSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '"><link type="' + get_symbol_type(
                            sym['lines'][v]['srcSymbol']) + '" >' + str(
                            node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                        if network:
                            f = False
                            for s in range(len(network)):
                                if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       view['option']['iptype'] + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '</open_server>'

        elif symbol['option']['symbol_type'] == '40033':
            if symbol['objectClass'] == '3001':
                option = symbol['option']
                content_xml += '<emu_router id="' + str(symbol['uid']) + '"><name>' + symbol[
                    'name'] + '</name><description>' + option['discription'] + '</description><hypervisor name="' + \
                               data[option['symbol_platform']]['name'] + '" type="' + data[option['symbol_personal']][
                                   'name'] + '"></hypervisor><serverip>' + option['serverip'] + '</serverip>'
                network = symbol['net']
                flag = False
                xnt = 0
                sym = symbol
                if len(sym['lines']) < 1:
                    if len(sym['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in sym['lines']:
                    # if not sym['lines'][v].isExpand:
                    if sym['lines'][v]['srcSymbol'] == sym['id']:
                        if nodes[i]['option']['symbol_type'] == '40033':
                            xnt += 1
                            content_xml += '<interface id="' + str(v) + '" boundary="0"><link type="' + get_symbol_type(
                                sym['lines'][v]['dstSymbol']) + '" >' + str(
                                node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'
                        else:
                            xnt += 1
                            content_xml += '<interface id="' + str(v) + '" boundary="1"><link type="' + get_symbol_type(
                                sym['lines'][v]['dstSymbol']) + '" >' + str(
                                node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'

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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                        if nodes[i]['option']['symbol_type'] == '40033':
                            xnt += 1
                            content_xml += '<interface id="' + str(v) + '" boundary="0"><link type="' + get_symbol_type(
                                sym['lines'][v]['srcSymbol']) + '" >' + str(
                                node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                        else:
                            xnt += 1
                            content_xml += '<interface id="' + str(v) + '" boundary="1"><link type="' + get_symbol_type(
                                sym['lines'][v]['srcSymbol']) + '" >' + str(
                                node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'

                        if network:
                            f = False
                            for s in range(len(network)):
                                if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '" boundary="0">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       view['option']['iptype'] + '</iptype>'
                        content_xml += '</interface>'

                if option['symbol_modchacked']:
                    # content_xml += '<template id="' + option['symbol_modchacked'] + '"></template>'
                    content_xml += '<template id="' + str(data[option['symbol_modchacked']]['value']) + '"></template>'
                else:
                    content_xml += '<template id="defalut"></template>'

                content_xml += '</emu_router>'
            elif symbol['objectClass'] == '3002':
                option = symbol['option']
                content_xml += '<emu_switch id="' + str(symbol['uid']) + '"><name>' + symbol[
                    'name'] + '</name><description>' + option['discription'] + '</description><hypervisor name="' + \
                               data[option['symbol_platform']]['name'] + '" type="' + data[option['symbol_personal']][
                                   'name'] + '"></hypervisor><serverip>' + option['serverip'] + '</serverip>'
                network = symbol['net']
                flag = False
                xnt = 0
                sym = symbol
                if len(sym['lines']) < 1:
                    if len(sym['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in sym['lines']:
                    # if not sym['lines'][v].isExpand:
                    if sym['lines'][v]['srcSymbol'] == sym['id']:
                        if nodes[i]['option']['symbol_type'] == '40033':
                            xnt += 1
                            content_xml += '<interface id="' + str(v) + '" boundary="0"><link type="' + get_symbol_type(
                                sym['lines'][v]['dstSymbol']) + '" >' + str(
                                node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'
                        else:
                            xnt += 1
                            content_xml += '<interface id="' + str(v) + '" boundary="1"><link type="' + get_symbol_type(
                                sym['lines'][v]['dstSymbol']) + '" >' + str(
                                node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'

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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                        if nodes[i]['option']['symbol_type'] == '40033':
                            xnt += 1
                            content_xml += '<interface id="' + str(v) + '" boundary="0"><link type="' + get_symbol_type(
                                sym['lines'][v]['srcSymbol']) + '" >' + str(
                                node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                        else:
                            xnt += 1
                            content_xml += '<interface id="' + str(v) + '" boundary="1"><link type="' + get_symbol_type(
                                sym['lines'][v]['srcSymbol']) + '" >' + str(
                                node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'

                        if network:
                            f = False
                            for s in range(len(network)):
                                if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '" boundary="0">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       view['option']['iptype'] + '</iptype>'
                        content_xml += '</interface>'

                if option['symbol_modchacked']:
                    # content_xml += '<template id="' + option['symbol_modchacked'] + '"></template>'
                    content_xml += '<template id="' + str(data[option['symbol_modchacked']]['value']) + '"></template>'
                else:
                    content_xml += '<template id="defalut"></template>'

                content_xml += '</emu_switch>'
            elif symbol['objectClass'] == '3003':
                option = symbol['option']
                content_xml += '<emu_host id="' + str(symbol['uid']) + '"><hypervisor name="' + \
                               data[option['symbol_platform']]['name'] + '"></hypervisor><name>' + symbol[
                                   'name'] + '</name><description>' + option['discription'] + '</description><vcpu>' + \
                               option['cpu'] + '</vcpu><memory>' + option['memory'] + '</memory><serverip>' + option[
                                   'serverip'] + '</serverip>'
                network = symbol['net']
                flag = False
                xnt = 0
                sym = symbol
                # logger.debug(sym)
                # logger.debug(len(sym['lines']))
                if len(sym['lines']) < 1:
                    if len(sym['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in sym['lines']:
                    # if not sym['lines'][v].isExpand:
                    if sym['lines'][v]['srcSymbol'] == sym['id']:
                        if nodes[i]['option']['symbol_type'] == '40033':
                            xnt += 1
                            content_xml += '<interface id="' + str(v) + '" boundary="0"><link type="' + get_symbol_type(
                                sym['lines'][v]['dstSymbol']) + '" >' + str(
                                node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'
                        else:
                            xnt += 1
                            content_xml += '<interface id="' + str(v) + '" boundary="1"><link type="' + get_symbol_type(
                                sym['lines'][v]['dstSymbol']) + '" >' + str(
                                node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'

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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                        if nodes[i]['option']['symbol_type'] == '40033':
                            xnt += 1
                            content_xml += '<interface id="' + str(v) + '" boundary="0"><link type="' + get_symbol_type(
                                sym['lines'][v]['srcSymbol']) + '" >' + str(
                                node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                        else:
                            xnt += 1
                            content_xml += '<interface id="' + str(v) + '" boundary="1"><link type="' + get_symbol_type(
                                sym['lines'][v]['srcSymbol']) + '" >' + str(
                                node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'

                        if network:
                            f = False
                            for s in range(len(network)):
                                if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '" boundary="0">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       view['option']['iptype'] + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '<os><type arch="' + data[option['symbol_cpumodel']]['name'] + '" machine="' + \
                               data[option['symbol_simulation']]['name'] + '">' + data[option['operating_systemk']][
                                   'name'] + '</type></os>'

                if option.get('installed', None):
                    # logger.debug('true')
                    content_xml += '<apps>';
                    for instas in option['installed'].split(','):
                        content_xml += '<app id="' + str(data[instas]['value']) + '"></app>'
                    content_xml += '</apps>'

                if option['symbol_modchacked']:
                    # content_xml += '<template id="' + option['symbol_modchacked'] + '"></template>'
                    content_xml += '<template id="' + str(data[option['symbol_modchacked']]['value']) + '"></template>'
                else:
                    content_xml += '<template id="defalut"></template>'

                content_xml += '</emu_host>'
            elif symbol['objectClass'] == '3004':
                option = symbol['option']
                content_xml += '<emu_server id="' + str(symbol['uid']) + '"><hypervisor name="' + \
                               data[option['symbol_platform']]['name'] + '"></hypervisor><name>' + symbol[
                                   'name'] + '</name><description>' + option['discription'] + '</description><vcpu>' + \
                               option['cpu'] + '</vcpu><memory>' + option['memory'] + '</memory><serverip>' + option[
                                   'serverip'] + '</serverip>'
                network = symbol['net']
                flag = False
                xnt = 0
                sym = symbol
                if len(sym['lines']) < 1:
                    if len(sym['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/></interface>'
                for v in sym['lines']:
                    # if not sym['lines'][v].isExpand:
                    if sym['lines'][v]['srcSymbol'] == sym['id']:
                        if nodes[i]['option']['symbol_type'] == '40033':
                            xnt += 1
                            content_xml += '<interface id="' + str(v) + '" boundary="0"><link type="' + get_symbol_type(
                                sym['lines'][v]['dstSymbol']) + '" >' + str(
                                node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'
                        else:
                            xnt += 1
                            content_xml += '<interface id="' + str(v) + '" boundary="1"><link type="' + get_symbol_type(
                                sym['lines'][v]['dstSymbol']) + '" >' + str(
                                node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'

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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                        if nodes[i]['option']['symbol_type'] == '40033':
                            xnt += 1
                            content_xml += '<interface id="' + str(v) + '" boundary="0"><link type="' + get_symbol_type(
                                sym['lines'][v]['srcSymbol']) + '" >' + str(
                                node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                        else:
                            xnt += 1
                            content_xml += '<interface id="' + str(v) + '" boundary="1"><link type="' + get_symbol_type(
                                sym['lines'][v]['srcSymbol']) + '" >' + str(
                                node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'

                        if network:
                            f = False
                            for s in range(len(network)):
                                if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
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
                                           view['option']['iptype'] + '</iptype>'

                        content_xml += '</interface>'
                        flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '" boundary="0">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       view['option']['iptype'] + '</iptype>'
                        content_xml += '</interface>'

                content_xml += '<os><type arch="' + data[option['symbol_cpumodel']]['name'] + '" machine="' + \
                               data[option['symbol_simulation']]['name'] + '">' + data[option['operating_systemk']][
                                   'name'] + '</type></os>'

                if option.get('installed', None):
                    content_xml += '<apps>'
                    for instas in option['installed'].split(','):
                        content_xml += '<app id="' + str(data[instas]['value']) + '"></app>'
                    content_xml += '</apps>'

                if option['symbol_modchacked']:
                    # content_xml += '<template id="' + option['symbol_modchacked'] + '"></template>'
                    content_xml += '<template id="' + str(data[option['symbol_modchacked']]['value']) + '"></template>'
                else:
                    content_xml += '<template id="defalut"></template>'

                content_xml += '</emu_server>'
            elif symbol['objectClass'] == '3005':
                option = symbol['option']
                content_xml += '<emu_ids id="' + str(symbol['uid']) + '"><name>' + symbol[
                    'name'] + '</name><description>' + option['discription'] + '</description><hypervisor name="' + \
                               data[option['symbol_platform']]['name'] + '"></hypervisor><serverip>' + option[
                                   'serverip'] + '</serverip>'
                network = symbol['net']
                flag = False
                xnt = 0
                sym = symbol
                if len(sym['lines']) < 1:
                    if len(sym['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                for v in sym['lines']:
                    # if not sym['lines'][v].isExpand:
                    if sym['lines'][v]['srcSymbol'] == sym['id']:
                        if nodes[i]['option']['symbol_type'] == '40033':
                            xnt += 1
                            content_xml += '<interface id="' + str(v) + '" boundary="0"><link type="' + get_symbol_type(
                                sym['lines'][v]['dstSymbol']) + '" >' + str(
                                node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'
                        else:
                            xnt += 1
                            content_xml += '<interface id="' + str(v) + '" boundary="1"><link type="' + get_symbol_type(
                                sym['lines'][v]['dstSymbol']) + '" >' + str(
                                node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'

                        if network:
                            f = False
                            for s in range(len(network)):
                                if network[s]['name'] == (sym['lines'][v]['dstSymbol'])[4:]:
                                    content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                                        'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><using_type>' + \
                                                   network[s]['port'] + '</using_type>'
                                    f = True
                                    break

                            if not f:
                                content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                               view['option']['iptype'] + '</iptype><using_type>1</using_type>'

                        else:
                            content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                           view['option']['iptype'] + '</iptype><using_type>1</using_type>'

                        content_xml += '</interface>'
                        flag = True

                    elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                        if nodes[i]['option']['symbol_type'] == '40033':
                            xnt += 1
                            content_xml += '<interface id="' + str(v) + '" boundary="0"><link type="' + get_symbol_type(
                                sym['lines'][v]['srcSymbol']) + '" >' + str(
                                node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                        else:
                            xnt += 1
                            content_xml += '<interface id="' + str(v) + '" boundary="1"><link type="' + get_symbol_type(
                                sym['lines'][v]['srcSymbol']) + '" >' + str(
                                node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'

                        if network:
                            f = False
                            for s in range(len(network)):
                                if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
                                    content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                                        'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><using_type>' + \
                                                   network[s]['port'] + '</using_type>'
                                    f = True
                                    break

                            if not f:
                                content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                               view['option']['iptype'] + '</iptype><using_type>1</using_type>'

                        else:
                            content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                           view['option']['iptype'] + '</iptype><using_type>1</using_type>'

                        content_xml += '</interface>'
                        flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '" boundary="0">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       view['option']['iptype'] + '</iptype><using_type>1</using_type>'
                        content_xml += '</interface>'

                if option.get('support0', False):
                    support = (option['support0']).split(',')
                    content_xml += '<rules>'
                    support_id = []
                    for su in range(len(support)):
                        support_id.append(data[support[su]]['value'])
                    # for su in range(len(support)):
                    #     for i in conf_rules['ids']:
                    #         logger.debug(i['rule_id'])
                    #         logger.debug(data[support[su]])
                    #         if i['rule_id'] == data[support[su]]['value']:
                    #             content_xml += '<rule id="' + data[support[su]]['value'] + '" enable="1"/>'
                    #         else:
                    #             content_xml += '<rule id="' + data[support[su]]['value'] + '" enable="0"/>'
                    # for su in range(len(support)):
                    # for i in conf_rules['ids']:
                    #     for su in range(len(support)):
                    #         # logger.debug(i['rule_id'])
                    #         # logger.debug(data[support[su]])
                    #         if i['rule_id'] == data[support[su]]['value']:
                    #             content_xml += ''
                    #             break
                    #         else:
                    #             content_xml += '<rule id="' + i['rule_id']  + '" enable="0"/>'
                    #             break
                    for i in conf_rules['ids']:
                        if i['rule_id'] in support_id:
                            content_xml += '<rule id="' + i['rule_id'] + '" enable="1"/>'
                        else:
                            content_xml += '<rule id="' + i['rule_id'] + '" enable="0"/>'
                    content_xml += '</rules>'
                else:
                    content_xml += '<rules></rules>'

                content_xml += '</emu_ids>'
            elif symbol['objectClass'] == '3006':
                option = symbol['option']
                content_xml += '<emu_ips id="' + str(symbol['uid']) + '"><name>' + symbol[
                    'name'] + '</name><description>' + option['discription'] + '</description><hypervisor name="' + \
                               data[option['symbol_platform']]['name'] + '"></hypervisor><serverip>' + option[
                                   'serverip'] + '</serverip>'
                network = symbol['net']
                flag = False
                xnt = 0
                sym = symbol
                if len(sym['lines']) < 1:
                    if len(sym['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                for v in sym['lines']:
                    # if not sym['lines'][v].isExpand:
                    if sym['lines'][v]['srcSymbol'] == sym['id']:
                        if nodes[i]['option']['symbol_type'] == '40033':
                            xnt += 1
                            content_xml += '<interface id="' + str(v) + '" boundary="0"><link type="' + get_symbol_type(
                                sym['lines'][v]['dstSymbol']) + '" >' + str(
                                node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'
                        else:
                            xnt += 1
                            content_xml += '<interface id="' + str(v) + '" boundary="1"><link type="' + get_symbol_type(
                                sym['lines'][v]['dstSymbol']) + '" >' + str(
                                node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'

                        if network:
                            f = False
                            for s in range(len(network)):
                                if network[s]['name'] == (sym['lines'][v]['dstSymbol'])[4:]:
                                    content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                                        'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><using_type>' + \
                                                   network[s]['port'] + '</using_type>'
                                    f = True
                                    break

                            if not f:
                                content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                               view['option']['iptype'] + '</iptype><using_type>1</using_type>'

                        else:
                            content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                           view['option']['iptype'] + '</iptype><using_type>1</using_type>'

                        content_xml += '</interface>'
                        flag = True

                    elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                        if nodes[i]['option']['symbol_type'] == '40033':
                            xnt += 1
                            content_xml += '<interface id="' + str(v) + '" boundary="0"><link type="' + get_symbol_type(
                                sym['lines'][v]['srcSymbol']) + '" >' + str(
                                node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                        else:
                            xnt += 1
                            content_xml += '<interface id="' + str(v) + '" boundary="1"><link type="' + get_symbol_type(
                                sym['lines'][v]['srcSymbol']) + '" >' + str(
                                node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'

                        if network:
                            f = False
                            for s in range(len(network)):
                                if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
                                    content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                                        'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><using_type>' + \
                                                   network[s]['port'] + '</using_type>'
                                    f = True
                                    break

                            if not f:
                                content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                               view['option']['iptype'] + '</iptype><using_type>1</using_type>'

                        else:
                            content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                           view['option']['iptype'] + '</iptype><using_type>1</using_type>'

                        content_xml += '</interface>'
                        flag = True

                    if not flag:
                        content_xml += '<interface id="' + str(v) + '" boundary="0">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       view['option']['iptype'] + '</iptype><using_type>1</using_type>'
                        content_xml += '</interface>'

                # if hasattr(option, 'support0'):
                #     support = (option['support0']).split(',')
                #     content_xml += '<rules>'
                #     for su in range(len(support)):
                #         content_xml += '<rule id="' + data[support[su]]['value'] + '" enable="1"/>'
                if option.get('support0', False):
                    support = (option['support0']).split(',')
                    support_id = []
                    for su in range(len(support)):
                        support_id.append(data[support[su]]['value'])
                    content_xml += '<rules>'

                    for i in conf_rules['ips']:
                        if i['rule_id'] in support_id:
                            content_xml += '<rule id="' + i['rule_id'] + '" enable="1"/>'
                        else:
                            content_xml += '<rule id="' + i['rule_id'] + '" enable="0"/>'

                    content_xml += '</rules>'
                else:
                    content_xml += '<rules></rules>'

                content_xml += '</emu_ips>'
            elif symbol['objectClass'] == '3007':
                option = symbol['option']
                content_xml += '<emu_firewall id="' + str(symbol['uid']) + '"><name>' + symbol[
                    'name'] + '</name><description>' + option['discription'] + '</description><hypervisor name="' + \
                               data[option['symbol_platform']]['name'] + '"></hypervisor><serverip>' + option[
                                   'serverip'] + '</serverip>'
                network = symbol['net']
                flag = False
                xnt = 0
                sym = symbol
                if len(sym['lines']) < 1:
                    if len(sym['net']):
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="' + \
                                       sym['net'][0]['ip'] + '" netmask="' + sym['net'][0][
                                           'subnetmask'] + '" gateway="' + sym['net'][0][
                                           'gateway'] + '"/><iptype address="' + sym['net'][0]['ip'] + '" netmask="' + \
                                       sym['net'][0]['subnetmask'] + '" gateway="' + sym['net'][0]['gateway'] + '">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                    else:
                        content_xml += '<interface id="0" boundary="0"><link type="empty" ></link><ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       view['option']['iptype'] + '</iptype></interface>'
                for v in sym['lines']:
                    # if not sym['lines'][v].isExpand:
                    if sym['lines'][v]['srcSymbol'] == sym['id']:
                        if nodes[i]['option']['symbol_type'] == '40033':
                            xnt += 1
                            content_xml += '<interface id="' + str(v) + '" boundary="0"><link type="' + get_symbol_type(
                                sym['lines'][v]['dstSymbol']) + '" >' + str(
                                node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'
                        else:
                            xnt += 1
                            content_xml += '<interface id="' + str(v) + '" boundary="1"><link type="' + get_symbol_type(
                                sym['lines'][v]['dstSymbol']) + '" >' + str(
                                node_dict[sym['lines'][v]['dstSymbol']]['uid']) + '</link>'

                        if network:
                            f = False
                            for s in range(len(network)):
                                if network[s]['name'] == (sym['lines'][v]['dstSymbol'])[4:]:
                                    content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                                        'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><using_type>' + \
                                                   network[s]['port'] + '</using_type>'
                                    f = True
                                    break

                            if not f:
                                content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                               view['option']['iptype'] + '</iptype><using_type>1</using_type>'

                        else:
                            content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                           view['option']['iptype'] + '</iptype><using_type>1</using_type>'

                        content_xml += '</interface>'
                        flag = True

                    elif sym['lines'][v]['dstSymbol'] == symbol['id']:
                        if nodes[i]['option']['symbol_type'] == '40033':
                            xnt += 1
                            content_xml += '<interface id="' + str(v) + '" boundary="0"><link type="' + get_symbol_type(
                                sym['lines'][v]['srcSymbol']) + '" >' + str(
                                node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'
                        else:
                            xnt += 1
                            content_xml += '<interface id="' + str(v) + '" boundary="1"><link type="' + get_symbol_type(
                                sym['lines'][v]['srcSymbol']) + '" >' + str(
                                node_dict[sym['lines'][v]['srcSymbol']]['uid']) + '</link>'

                        if network:
                            f = False
                            for s in range(len(network)):
                                if network[s]['name'] == (sym['lines'][v]['srcSymbol'])[4:]:
                                    content_xml += '<ip address="' + network[s]['ip'] + '" netmask="' + network[s][
                                        'subnetmask'] + '" gateway="' + network[s]['gateway'] + '"/><using_type>' + \
                                                   network[s]['port'] + '</using_type>'
                                    f = True
                                    break

                            if not f:
                                content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                               view['option']['iptype'] + '</iptype><using_type>1</using_type>'

                        else:
                            content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                           view['option']['iptype'] + '</iptype><using_type>1</using_type>'

                        content_xml += '</interface>'
                        flag = True

                    if not flag:
                        xnt += 1
                        content_xml += '<interface id="' + str(v) + '" boundary="0">'
                        content_xml += '<ip address="default" netmask="default" gateway="default"/><iptype address="default" netmask="default" gateway="default">' + \
                                       view['option']['iptype'] + '</iptype><using_type>1</using_type>'
                        content_xml += '</interface>'

                # if hasattr(option, 'support0'):
                #     support = (option['support0']).split(',')
                #     content_xml += '<rules>'
                #     for su in range(len(support)):
                #         content_xml += '<rule id="' + data[support[su]]['value'] + '" enable="1"/>'
                # logger.debug(option)
                # try:
                #
                # except:
                #     content_xml += '<rules></rules>'
                # logger.debug(option.get('support0',True))
                # logger.debug(option)
                # logger.debug(hasattr(option,'support0'))
                if option.get('support0', False):
                    support = (option['support0']).split(',')
                    content_xml += '<rules>'
                    support_id = []
                    for su in range(len(support)):
                        support_id.append(data[support[su]]['value'])

                    for i in conf_rules['fw']:
                        if i['rule_id'] in support_id:
                            content_xml += '<rule id="' + i['rule_id'] + '" enable="1"/>'
                        else:
                            content_xml += '<rule id="' + i['rule_id'] + '" enable="0"/>'

                    content_xml += '</rules>'
                else:
                    content_xml += '<rules></rules>'

                if symbol['filter']:
                    filter = symbol['filt']
                    content_xml += '<portfilter>'

                    for d in range(len(filter)):
                        content_xml += '<rule port="' + filter[d]['port'] + '" direction="' + filter[d][
                            'direction'] + '" pass="' + filter[d]['pass'] + '"/>'

                    content_xml += '</portfilter>'
                else:
                    content_xml += '<portfilter></portfilter>'

                content_xml += '</emu_firewall>'

    content_xml += '</root>'
    f = open(path, "w")
    f.write(content_xml)
    f.close()
    return content_xml
