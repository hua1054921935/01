def build_suplarge(task_id=None, case_id=None, person_id=None, view=None):
    # reload(sys)
    # sys.setdefaultencoding('utf-8')

    db = database.DB()
    db.connect()
    result = {'flag': False}

    # logger.debug('#'*10)
    # return HttpResponse(json.dumps(result, default=utils.json_encoder))
    case_path = os.path.join(settings.NFS_ROOT, 'CaseDefinitions')
    sql_one = """
        update b_topic_task set recv_msg = '%s', recv_time = now(), state = '%s', duration = %s
        where taskid = %s
    """
    begin = datetime.datetime.now()
    if not os.path.exists(case_path):
        info = "nfs not mount"
        result['info'] = info
        db.execute_sql(sql_one % (info, '1', 0, task_id))
        db.close()
        return result

    a_dir = os.path.join(case_path, str(case_id), case_dir['a'])
    m_dir = os.path.join(case_path, str(case_id), case_dir['m'])
    p_dir = os.path.join(case_path, str(case_id), case_dir['p'])
    t_dir = os.path.join(case_path, str(case_id), case_dir['t'])

    if not os.path.exists(a_dir):
        os.makedirs(a_dir)
    if not os.path.exists(m_dir):
        os.makedirs(m_dir)
    if not os.path.exists(p_dir):
        os.makedirs(p_dir)
    if not os.path.exists(t_dir):
        os.makedirs(t_dir)

    os.chmod(m_dir, stat.S_IRWXU + stat.S_IRWXG + stat.S_IRWXO)

    sql = """
        select topological_id from b_topological_structure where case_id = '%s'
    """ % (case_id)

    # delete b_topological_structure  b_topological_relation b_node b_node_interface a_node_conf_rules a_port_filter
    # logger.debug('one must %s seconds' % (time.time()-start))
    topological_id = db.query_sql(sql)
    if len(topological_id) > 0:
        sql = """
            delete from b_topological_structure
            where case_id = '%s'
        """ % (case_id)
        db.execute_sql(sql)
        # topological_node = []
        for value in topological_id:
            sql = """
                delete from b_node_interface where node_id in (select node_id from b_node where  topological_id = %s)
            """ % (value['topological_id'])
            db.execute_sql(sql)
            sql = """
                delete from a_port_filter where node_id in (select node_id from b_node where  topological_id = %s)
            """ % (value['topological_id'])
            db.execute_sql(sql)
            sql = """
                delete from a_node_conf_rules where node_id in (select node_id from b_node where  topological_id = %s)
            """ % (value['topological_id'])
            db.execute_sql(sql)
            sql = """
                delete from b_node where topological_id = %s
            """ % (value['topological_id'])
            db.execute_sql(sql)
            sql = """
                delete from b_topological_relation where topological_id = %s
            """ % (value['topological_id'])
            db.execute_sql(sql)
            # topological_node.append(node_id)
    else:
        pass

    # 插入新数据至b_topological_structure
    sql = """
        INSERT INTO b_topological_structure
        (
          topological_name,topological_discription,draw_type,delay,datarate,mtu,create_time,person_id,status,case_id
        )
        VALUE
        (
          '%s','%s','large',%s,%s,%s,now(),%s,'1','%s'
        )
    """ % (
    view['name'], view['descr'], view['option']['delay'], view['option']['datarate'], view['option']['mtu'], person_id,
    case_id)

    topological_id = db.execute_sql(sql)

    # 获取节点的ownership_type
    ownership_type = "202001"
    sql = """
        select code_id from sys_code_dict where dict_id = "NEUTRAL"
    """
    res = db.query_sql(sql)
    for i in res:
        if i['code_id'] is not None:
            ownership_type = i['code_id']

    # 插入新数据至b_node
    sql = """
        select * from a_all_conf_rules
    """
    res = db.query_sql(sql)

    conf_rules = {}
    for v in res:
        if not conf_rules.get(v['using_type'], False):
            conf_rules[v['using_type']] = []
        conf_rules[v['using_type']].append(v)

    view['min'] = 0
    view['max'] = 0

    xxx = time.time()
    topo_data = create_topo(view)
    # logger.debug('topo_data' + str(time.time() - xxx))
    # print 'topo_data'+str(time.time()-xxx)
    # topo_data = create_topo_three(view)

    # topo_data = get_data_topo1(view)

    node_dict = {}

    xxxx = time.time()
    sql = """
        insert into b_node
        (
          base_node_id, node_name, node_category,node_type,nic_number,topological_id,ownership_type, hypervisor, memory, cpu_number, node_os, arch, machine, vm_template_id
        )
        values
    """
    for tags in topo_data:
        node = {}
        # topo_data[tag]['node_discription'] = 'node'
        node['node_name'] = 'server' + '_' + str(tags)
        node['node_category'] = topo_data[tags]['node_category']
        node['node_type'] = topo_data[tags]['node_type']
        node['nic_number'] = len(topo_data[tags]['line'])
        node['topological_id'] = topological_id
        node['ownership_type'] = view['node_template']['ownership_type']
        node['hypervisor'] = view['node_template']['hypervisor']
        node['memory'] = view['node_template']['memory']
        node['cpu_number'] = view['node_template']['cpu_number']
        node['node_os'] = view['node_template']['node_os']
        node['arch'] = view['node_template']['arch']
        node['machine'] = view['node_template']['machine']
        node['vm_template_id'] = view['node_template']['vm_template_id']
        params = (0，
        node['node_name'], node['node_category'], node['node_type'], node['nic_number'],node['topological_id'],
        node['ownership_type'],
        node['hypervisor'], node['memory'], node['cpu_number'], node['node_os'], node['arch'], node['machine'],
        node['vm_template_id']
        )
        # prefix = str(params)


        sql += str(params) + ',' + '\n\t'
    sql=sql.rsplit(',', 1)[0]
    first_node_id = db.execute_sql(sql)
    first_node_id = int(first_node_id)
    for tag in topo_data:
        # logger.debug('ok')
        node = {}
        # topo_data[tag]['node_discription'] = 'node'
        node['node_name'] = 'server' + '_' + str(tag)
        node['node_category'] = topo_data[tag]['node_category']
        node['node_type'] = topo_data[tag]['node_type']
        node['nic_number'] = len(topo_data[tag]['line'])
        node['topological_id'] = topological_id
        node['ownership_type'] = view['node_template']['ownership_type']
        node['hypervisor'] = view['node_template']['hypervisor']
        node['memory'] = view['node_template']['memory']
        node['cpu_number'] = view['node_template']['cpu_number']
        node['node_os'] = view['node_template']['node_os']
        node['arch'] = view['node_template']['arch']
        node['machine'] = view['node_template']['machine']
        node['vm_template_id'] = view['node_template']['vm_template_id']
        node['id']=first_node_id
        node_dict[str(node['id'])] = node
        if view['min'] == 0:
            view['min'] = node['id']
        view['max'] = node['id']
        topo_data[tag]['id'] = node['id']
        prefix = """
            INSERT INTO b_node_interface(interface_id, node_id, link_node_id, nic_ip_address, nic_subnet_mask, gateway)
            VALUES """
        lines = topo_data[tag]['line']

        if node['nic_number'] > 0:
            for id_ in lines:
                interface_id = lines.index(id_)
                node_id = topo_data[tag]['id']
                link_node_id = id_
                nic_ip_address = 'default'
                nic_subnet_mask = 'default'
                gateway = 'default'
                params = (interface_id, node_id, link_node_id, nic_ip_address, nic_subnet_mask, gateway)
                # prefix = str(params)
                prefix += str(params) + ',' + '\n\t'

            sql_three = prefix.rsplit(',', 1)[0]
            db.execute_sql(sql_three)
    # logger.debug('for tag' + str(time.time() - xxxx))
        first_node_id+=1


    sql = """
        select code_id from sys_code_dict where dict_id = "DEFINED"
    """
    res = db.query_sql(sql)
    define_code_id = "200501"
    for i in res:
        if i['code_id'] is not None:
            define_code_id = i['code_id']

    case_path_base = 'CaseDefinitions'
    a_file_base = os.path.join(case_path_base, str(case_id), case_dir['a'], 'a' + str(topological_id) + '.xml')
    m_file_base = os.path.join(case_path_base, str(case_id), case_dir['m'], 'm' + str(topological_id) + '.xml')
    p_file_base = os.path.join(case_path_base, str(case_id), case_dir['p'], 'p' + str(topological_id) + '.xml')
    t_file_base = os.path.join(case_path_base, str(case_id), case_dir['t'], 't' + str(topological_id) + '.xml')

    sql = """
        select * from b_case where case_id='%s'
    """ % case_id
    res = db.query_sql(sql)

    if len(res) > 0:
        # logger.debug(t_file_base)
        # 更新数据至b_case
        sql = """
            update b_case set name='%s', description='%s', updator_id=%s, update_time=now(), state='%s',tfile='%s'
            where case_id='%s'
        """ % (view['name'], view['descr'], person_id, define_code_id, t_file_base, case_id)
        # logger.debug(sql)
        rrrr = db.update_sql(sql)
        # logger.debug(rrrr)
    else:
        # 插入新数据至b_case
        sql = """
            insert into b_case(case_id, base_case_id, is_template, name, tfile, afile, mfile, pfile, state, field_oriented,creator_id, create_time, updator_id, update_time, description)
            values('%s', '%s', '1', '%s', '%s', '%s', '%s', '%s','%s', '%s', %s, now(), %s, now(), '%s')
        """ % (case_id, '0', view['name'], t_file_base, a_file_base, m_file_base, p_file_base, define_code_id,
               view['field_oriented'], person_id, person_id, view['descr'])
        db.execute_sql(sql)
    t_file = 't' + str(case_id) + '.xml'

    case_paths = os.path.join(case_path, case_id, 'topology.json')
    xxxxx = time.time()
    with open(case_paths, 'wb') as f:
        json.dump(topo_data, f)
    # logger.debug('topology.json' + str(time.time() - xxxxx))

    xxxxxx = time.time()
    create_t_xml(os.path.join(case_path, str(case_id), t_file), topo_data, view, node_dict)
    # logger.debug('create_t_xml' + str(time.time() - xxxxxx))

    h_file = 'h' + str(case_id) + '.xml'
    with open(os.path.join(case_path, str(case_id), h_file), 'wb') as f:
        f.write('')

    v_file = 'v' + str(case_id) + '.xml'
    with open(os.path.join(case_path, str(case_id), v_file), 'wb') as f:
        f.write('')
    xxxxxxx = time.time()
    create_t_file(os.path.join(t_dir, 't' + str(topological_id) + '.xml'), topo_data, view, node_dict)
    # logger.debug('create_t_file' + str(time.time() - xxxxxxx))
    sql = """
        INSERT INTO
        b_topological_relation
        (
          topological_id,back_xml_name,view_xml_name,list_xml_name
        )
        VALUE
        (
          %s,'%s','%s','%s'
        )
    """ % (topological_id, t_file, v_file, h_file)
    db.execute_sql(sql)


    os.chmod(case_paths, stat.S_IRWXU + stat.S_IRWXG + stat.S_IRWXO)

    result['flag'] = True
    result['id'] = case_id
    end = datetime.datetime.now()
    second = (end - begin).seconds
    db.execute_sql(sql_one % ('', '2', second, task_id))
    db.close()
    return result
