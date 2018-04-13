import tower_cli
import json
import os


vars = """---
connection: local
ansible_ssh_host: 127.0.0.1"""


# helper method to standardize printing
def create(res_type, **kwargs):
    print ''
    print '  --- Creating {} : {} ---'.format(res_type, kwargs.get('name'))
    res = tower_cli.get_resource(res_type)
    r = res.create(**kwargs)
    print json.dumps(r, indent=4)
    return r['id']


# environmental setup
o = create('organization', name='Default')
i = create('inventory', name='localhost', variables=vars, organization=o)
create('host', inventory=i, variables=vars, name='127.0.0.1')
p = create('project',
           wait=True, name='callback-testing-playbooks',
           scm_url='https://github.com/AlanCoding/callback-testing-playbooks.git',
           scm_type='git',
           organization=o)


# Create JT that corresponds to each testing playbook
jt_ids = []
for path in os.listdir('.'):
    if '.git' in path:
        continue
    if os.path.isdir(path):
        for filename in os.listdir(path):
            rel_path = os.path.join(path, filename)
            jt_name = 'test_callbacks_{}'.format(rel_path)
            jt = create('job_template',
                        name=jt_name, inventory=i,
                        project=p,
                        playbook=rel_path)
            jt_ids.append(jt)


# not waiting for jobs to finish, just fire them off
for jt in jt_ids:
    res = tower_cli.get_resource('job')
    print res.launch(job_template=jt)

