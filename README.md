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
names = [test_name for test_name in locals().keys() if test_name.startswith('test_')]
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

In order to make a PR against this repo, you probably want to do this
at the base folder of your AWX clone on your personal computer:

```
git clone https://github.com/AlanCoding/callback-testing-playbooks.git
```

Then, with the above code pasted into the test file, run the python file,
and assuming `BASE_DIR` is kept the same, it should produce a meaningful
diff with updates to the playbooks.

#### How do I run these inside of AWX

You need to install tower-cli and configure your login.
You need a user with a username `admin`, and you must, yourself, be a
superuser.

```
python run.py
```

That should create and run job templates for these playbooks.

(making new commit, ignore)
