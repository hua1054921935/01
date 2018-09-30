def create_t_xml(path, topo_data, view, node_dict):
    """
    :return: t1234567890.xml
    """

    def get_symbol_type(id):

        for id_index in topo_data:
            if topo_data[id_index]['id'] == id:
                t = node_dict[id]

        l_start = ""
        l_end = ""
        # if t['option']['symbol_type'] == '40031':
        #     l_start = "mms_"
        # elif t['option']['symbol_type'] == '40032':
        #     l_start = ""
        # elif t['option']['symbol_type'] == '40033':
        #     l_start = "emu_"
        # elif t['option']['symbol_type'] == '40034':
        #     l_start = "real_"
        # elif t['option']['symbol_type'] == '40035':
        #     l_start = "con_"
        # elif t['option']['symbol_type'] == '40036':
        #     l_start = "open_"

        if t['node_type'] == 'r':
            return l_start + "router"
        elif t['node_type'] == 's':
            return l_start + "switch"
        elif t['node_type'] == 'h':
            return l_start + "host"
        elif t['node_type'] == 'server':
            return l_start + "v"
        elif t['node_type'] == 'd':
            return l_start + "ids"
        elif t['node_type'] == 'p':
            return l_start + "ips"
        elif t['node_type'] == 'f':
            return l_start + "firewall"

    content_xml = '<diagram ratio="0.37971082126890027" layout="hierarchicalCyclic">'

    for i in topo_data:
        # if symbols['option']:
        #     content_xml += '<node id="' + str(symbols['uid']) + '" dx="' + str(symbols['x']) + '" dy="' + str(symbols['y']) + '" width="60.00" height="60.00"><infraStructure uid="' + str(get_symbol_type(symbols['id'])) + '" description="' + str(symbols['option']['discription']) + '" anchors="null" canBeLinkSource="false" canBeLinkTarget="false"/></node>'
        # else:
        content_xml += '<node id="' + str(topo_data[i]['id']) + '" dx="' + str(topo_data[i]['site'][0]) + '" dy="' + str(topo_data[i]['site'][1]) + '" dz="' + str(topo_data[i]['site'][2]) + '" width="60.00" height="60.00"><infraStructure uid="' + str(get_symbol_type(topo_data[i]['id'])) + '" description="''" anchors="null" canBeLinkSource="false" canBeLinkTarget="false"/></node>'
    for i in topo_data:
        line=topo_data[i]['line']
        for j in line:
            try:
                src = str(topo_data[i]['id'])
                dst = str(topo_data[j]['id'])
                content_xml += '<link id="' + src + '>' + dst + '" controlPoints="' + 'lines[j]['path']' + '" target="' + dst + '" source="' + src + '" linkLine="1" dataModelID="' + src + '>' + dst + '"><style/><data/></link>'
            except:
                print

    content_xml += '</diagram>'
    f = open(file, "w")
    f.write(content_xml)
    f.close()
