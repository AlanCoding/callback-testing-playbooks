### Playbooks from callback plugin tests

This repo has playbooks that are used in fixtures inside of `awx/lib/tests/`
inside of the AWX source control.

#### How do I re-generate these?

Insert the following code at the end of the file `test_display_callback.py`
in that test directory, and then simply run
`python awx/lib/tests/test_display_callback.py` inside of the AWX container,
from the project root (assuming dev setup).


```python
BASE_DIR = 'callback-testing-playbooks'
for name in names:
    print('')
    print('Processing test {}'.format(name))
    bare_name = name[len('test_callback_plugin_'):]
    if not os.path.exists('{}/{}'.format(BASE_DIR, bare_name)):
        os.makedirs('{}/{}'.format(BASE_DIR, bare_name))
    the_test = locals()[name]
    inputs = the_test.parametrize.args[1]
    for input in inputs:
        for k, v in input.items():
            filename = '{}/{}/{}'.format(BASE_DIR, bare_name, k)
            print('  Writing file {}'.format(filename))
            if not os.path.exists(filename):
                with open(filename, 'w') as f:
                    f.write(v)
```

