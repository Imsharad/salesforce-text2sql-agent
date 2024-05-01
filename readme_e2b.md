# Code Execution

You can execute code using the notebook module, using the `execCell` method. The method takes a string of code as an argument and returns an object with the results of the execution.

![](https://e2b.dev/docs/_next/static/media/node.ffbff9e8.svg)JavaScript & TypeScript

![](https://e2b.dev/docs/_next/static/media/python.c624d255.svg)Python

```python
import CodeInterpreter from e2b_code_interpreter

code ="print('Hello, World!')"

sandbox = CodeInterpreter.create()
execution = sandbox.notebook.exec_cell(code)
```

Copy**Copied!**

The `execCell` method also accepts following optional arguments:

* `kernel id`: The ID of the kernel to execute the code on. If not provided, the default kernel is used. See [here](https://e2b.dev/docs/code-interpreter/kernels) for more info on kernels.
* `on stdout`: A callback function to handle standard output messages from the code execution.
* `on_stderr`: A callback function to handle standard error messages from the code execution.
* `on_result`: A callback function to handle the result and display calls of the code execution.

## [Streaming response](https://e2b.dev/docs/code-interpreter/execution#streaming-response)

You can use the `on_*` callbacks to handle the output of the code execution as it happens. This is useful for long-running code. You can stream the output to the user as it is generated.

## [Execution object](https://e2b.dev/docs/code-interpreter/execution#execution-object)

The object returned by the `exec cell` method is little bit more complex, it's based on Jupyter. Here's an detailed explanation in the [Jupyter documentation](https://jupyter-client.readthedocs.io/en/stable/messaging.html).

It contains the following fields:

* `results`: A list containing result of the cell (interactively interpreted last line) and display calls (e.g. matplotlib plots).
* `logs`: Logs printed to stdout and stderr during execution.
* `error`: An error message, if there was an error during execution of the cell. It works only for Python code, not for system (`!` e.g `!pip install e2b`) commands.

### Result object

This object can be created in two different ways:

* Evaluation of the last line: If the last line of the code is an expression, the result is the value of that expression. As you would expect in REPL environments.
* Display calls: Calls to display functions, which can be used to display rich output in the notebook. E.g. [`img.show()`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.show.html), [`display(img)`](https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html), etc.

Represents the data to be displayed as a result of executing a cell in a Jupyter notebook. The result is similar to the structure returned by [ipython kernel](https://ipython.readthedocs.io/en/stable/development/execution.html#execution-semantics)

The result can contain multiple types of data, such as text, images, plots, etc. Each type of data is represented as a string, and the result can contain multiple types of data. The display calls don't have to have text representation, it's always present for the actual result, the other representations are optional.

The result has those basic data types:

#### Text types:

* `text`: text representation of the result
* `html`: html representation of the result
* `markdown`: markdown representation of the result
* `latex`: latex representation of the result

#### Image types:

* `png`: "base64 encoded png image",
* `jpeg`: "base64 encoded jpeg image",
* `svg`": "svg image",

#### Other types:

* `json`: "json representation",
* `javascript`: "javascript representation",
* `pdf`: "base64 encoded pdf"

If you want to integrate your own display formats or how to implement them for your classes, you can read more in [here](https://github.com/ipython/ipython/blob/main/examples/IPython%20Kernel/Custom%20Display%20Logic.ipynb)

### Logs object

Logs printed to stdout and stderr during execution. Examples of logs are print statements, warnings, subprocess output, etc.

It contains two fields:

* `stdout`: List of strings, each string is a line printed to stdout.
* `stderr`: List of strings, each string is a line printed to stderr.

### Error object

An error message, if there was an error during execution of the cell.

It works only for Python code, not for system (e.g. `!pip install non_existent_package`) commands. The system commands are executed in a separate process and the output is in stdout/stderr.

It contains three fields:

* `name`: Name of the error, e.g. `NameError`, `ValueError`, etc.
* `value`: Value of the error, e.g. `name 'non_existent_variable' is not defined`, etc.
* `traceback`: Traceback of the error.

## [Example how to interpret the results to LLM](https://e2b.dev/docs/code-interpreter/execution#example-how-to-interpret-the-results-to-llm)

Here's an example how to return the results to LLM:

![](https://e2b.dev/docs/_next/static/media/node.ffbff9e8.svg)JavaScript & TypeScript

![](https://e2b.dev/docs/_next/static/media/python.c624d255.svg)Python

```python
code ="<CODE GENERATED BY LLM>"
execution = sandbox.notebook.exec_cell(code)

# There was an error during execution, return the error and its traceback
if execution.error:
return (
f"There was an error during execution: {execution.error.name}: {execution.error.value}.\n"
f"{execution.error.traceback}"
    )

# The execution has some result, summarize to LLM, what are the results
if execution.results:
    message ="These are results of the execution:\n"
for i, result inenumerate(execution.results):
        message +=f"Result {i +1}:\n"
if result.is_main_result:
            message +=f"[Main result]: {result.text}\n"
else:
            message +=f"[Display data]: {result.text}\n"

if result.formats():
            message +=f"It has also following formats: {result.formats()}\n"

return message

# There were no results, check if there was something is stdout/err
if execution.logs.stdout or execution.logs.stderr:
    message ="There was no result of the execution, but here are the logs:\n"
if execution.logs.stdout:
        message +="Stdout: "+"\n".join(execution.logs.stdout)+"\n"

if execution.logs.stderr:
        message +="Stderr: "+"\n".join(execution.logs.stderr)+"\n"

return message

return"There was no output of the execution."
```

Minimal example with the sharing context

The following example demonstrates how to create a shared context between multiple code executions. This is useful when you want to share variables between different code cells.

JavaScript & TypeScript

Python
from e2b_code_interpreter import CodeInterpreter

with CodeInterpreter() as sandbox:
    sandbox.notebook.exec_cell("x = 1")

    execution = sandbox.notebook.exec_cell("x+=1; x")
    print(execution.text)  # outputs 2

Copy
Copied!
Get charts and any display-able data

JavaScript & TypeScript

Python
import base64
import io

from matplotlib import image as mpimg, pyplot as plt

from e2b_code_interpreter import CodeInterpreter

code = """
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 20, 100)
y = np.sin(x)

plt.plot(x, y)
plt.show()
"""

with CodeInterpreter() as sandbox:
    # you can install dependencies in "jupyter notebook style"
    sandbox.notebook.exec_cell("!pip install matplotlib")

    # plot random graph
    execution = sandbox.notebook.exec_cell(code)




# Examples

Here are some examples of how to use the E2B Code Interpreter package. If you are missing something, please let us know.

## [Minimal example with the sharing context](https://e2b.dev/docs/code-interpreter/examples#minimal-example-with-the-sharing-context)

The following example demonstrates how to create a shared context between multiple code executions. This is useful when you want to share variables between different code cells.

![](https://e2b.dev/docs/_next/static/media/node.ffbff9e8.svg)JavaScript & TypeScript

![](https://e2b.dev/docs/_next/static/media/python.c624d255.svg)Python

```python
from e2b_code_interpreter import CodeInterpreter

withCodeInterpreter()as sandbox:
    sandbox.notebook.exec_cell("x = 1")

    execution = sandbox.notebook.exec_cell("x+=1; x")
print(execution.text)# outputs 2

```

Copy**Copied!**

## [Get charts and any display-able data](https://e2b.dev/docs/code-interpreter/examples#get-charts-and-any-display-able-data)

![](https://e2b.dev/docs/_next/static/media/node.ffbff9e8.svg)JavaScript & TypeScript

![](https://e2b.dev/docs/_next/static/media/python.c624d255.svg)Python

```python
import base64
import io

from matplotlib import image as mpimg, pyplot as plt

from e2b_code_interpreter import CodeInterpreter

code ="""
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 20, 100)
y = np.sin(x)

plt.plot(x, y)
plt.show()
"""

withCodeInterpreter()as sandbox:
# you can install dependencies in "jupyter notebook style"
    sandbox.notebook.exec_cell("!pip install matplotlib")

# plot random graph
    execution = sandbox.notebook.exec_cell(code)

# there's your image
image = execution.results[0].png

# example how to show the image / prove it works
i = base64.b64decode(image)
i = io.BytesIO(i)
i = mpimg.imread(i, format='PNG')

plt.imshow(i, interpolation='nearest')
plt.show()
```

Copy**Copied!**

## [Streaming code output](https://e2b.dev/docs/code-interpreter/examples#streaming-code-output)

![](https://e2b.dev/docs/_next/static/media/node.ffbff9e8.svg)JavaScript & TypeScript

![](https://e2b.dev/docs/_next/static/media/python.c624d255.svg)Python

```python
from e2b_code_interpreter import CodeInterpreter

code ="""
import time
import pandas as pd

print("hello")
time.sleep(3)
data = pd.DataFrame(data=[[1, 2], [3, 4]], columns=["A", "B"])
display(data.head(10))
time.sleep(3)
print("world")
"""
withCodeInterpreter()as sandbox:
    sandbox.notebook.exec_cell(code, on_stdout=print, on_stderr=print, on_result=(lambdaresult: print(result.text)))
```








# Setting environment variables

## [Global environment variables](https://e2b.dev/docs/sandbox/api/envs#global-environment-variables)

You can set the sandbox's global environment variables when initializing a new sandbox.

![](https://e2b.dev/docs/_next/static/media/node.ffbff9e8.svg)JavaScript & TypeScript

![](https://e2b.dev/docs/_next/static/media/python.c624d255.svg)Python

```python
from e2b import Sandbox

sandbox =Sandbox(
    template="base",
    env_vars={"FOO": "Hello"},  
)

sandbox.close()
```

Copy**Copied!**

## [Environment variables per process](https://e2b.dev/docs/sandbox/api/envs#environment-variables-per-process)

Alternatively, you can set environment variables when starting a new process. These environment variables are accessible only for this process.

Environment variables set when starting a new process have precedence over the environment variables set when initializing the sandbox.

![](https://e2b.dev/docs/_next/static/media/node.ffbff9e8.svg)JavaScript & TypeScript

![](https://e2b.dev/docs/_next/static/media/python.c624d255.svg)Python

```python
from e2b import Sandbox

sandbox =Sandbox(
    template="base",
    env_vars={"FOO": "Hello"}
)

proc = sandbox.process.start(
"echo $FOO $BAR!",
    env_vars={"BAR": "World"},  
)
proc.wait()

print(proc.output.stdout)
# output: Hello World!

sandbox.close()
```






# File system (sandbox)

## [List directory](https://e2b.dev/docs/sandbox/api/filesystem#list-directory)

![](https://e2b.dev/docs/_next/static/media/node.ffbff9e8.svg)JavaScript & TypeScript

![](https://e2b.dev/docs/_next/static/media/python.c624d255.svg)Python

```python
from e2b import Sandbox

sandbox =Sandbox(template="base")

# List the root directory
content = sandbox.filesystem.list("/")
for item in content:
print(f"Is '{item.name}' directory?", item.is_dir)

sandbox.close()
```

Copy**Copied!**

## [Create directory](https://e2b.dev/docs/sandbox/api/filesystem#create-directory)

Create directory and all parent directories.

![](https://e2b.dev/docs/_next/static/media/node.ffbff9e8.svg)JavaScript & TypeScript

![](https://e2b.dev/docs/_next/static/media/python.c624d255.svg)Python

```python
from e2b import Sandbox

sandbox =Sandbox(template="base")

# Create a new directory '/dir'
sandbox.filesystem.make_dir("/dir")

sandbox.close()
```

Copy**Copied!**

## [Write to file](https://e2b.dev/docs/sandbox/api/filesystem#write-to-file)

When writing to a file that doesn't exist, the file will get created.

When writing to a file that already exists, the file will get overwritten.

When writing to a file that's in a directory that doesn't exist, you'll get an error.

![](https://e2b.dev/docs/_next/static/media/node.ffbff9e8.svg)JavaScript & TypeScript

![](https://e2b.dev/docs/_next/static/media/python.c624d255.svg)Python

```python
from e2b import Sandbox

sandbox =Sandbox(template="base")

# `filesystem.write()` will:
# - create the file if it doesn't exist
# - fail if any directory in the path doesn't exist
# - overwrite the file if it exists

# Write the content of the file '/hello.txt'
sandbox.filesystem.write("/hello.txt", "Hello World!")

# The following would fail because '/dir' doesn't exist
# sandbox.filesystem.write("/dir/hello.txt", "Hello World!")

sandbox.close()
```

Copy**Copied!**

## [Read from file](https://e2b.dev/docs/sandbox/api/filesystem#read-from-file)

![](https://e2b.dev/docs/_next/static/media/node.ffbff9e8.svg)JavaScript & TypeScript

![](https://e2b.dev/docs/_next/static/media/python.c624d255.svg)Python

```python
from e2b import Sandbox

sandbox =Sandbox(template="base")

# Read the '/etc/hosts' file
file_content = sandbox.filesystem.read("/etc/hosts")

# Prints something like:
# 127.0.0.1       localhost
print(file_content)

sandbox.close()
```

Copy**Copied!**

## [Write bytes](https://e2b.dev/docs/sandbox/api/filesystem#write-bytes)

![](https://e2b.dev/docs/_next/static/media/node.ffbff9e8.svg)JavaScript & TypeScript

![](https://e2b.dev/docs/_next/static/media/python.c624d255.svg)Python

```python
from e2b import Sandbox

sandbox =Sandbox(template="base")

content_in_bytes =bytearray(b"Hello world")

# `write_bytes` will write bytearray to a file inside the playground.
sandbox.filesystem.write_bytes("/file", content_in_bytes)

# We can read the file back to verify the content
file_content = sandbox.filesystem.read("/file")
print(file_content)

sandbox.close()
```

Copy**Copied!**

## [Read bytes](https://e2b.dev/docs/sandbox/api/filesystem#read-bytes)

![](https://e2b.dev/docs/_next/static/media/node.ffbff9e8.svg)JavaScript & TypeScript

![](https://e2b.dev/docs/_next/static/media/python.c624d255.svg)Python

```python
from e2b import Sandbox

sandbox =Sandbox(template="base")

# File bytes will read file's content as bytes
# `file_bytes` as a bytearray
file_bytes = sandbox.filesystem.read_bytes("/etc/hosts")

# The output will look similar to this:
# b'127.0.0.1\tlocalhost\n::1\tlocalhost ip6-localhost ip6-loopback\nfe00::0\tip6-localnet\nff00::0\tip6-mcastprefix\nff02::1\tip6-allnodes\nff02::2\tip6-allrouters\n172.17.0.17\t77c7a543226b\n'
print(file_bytes)

# We can save those bytes to a file locally like this:
withopen("./hosts.txt", "wb")as f:
    f.write(file_bytes)

sandbox.close()
```

Copy**Copied!**

## [Watch directory for changes](https://e2b.dev/docs/sandbox/api/filesystem#watch-directory-for-changes)

![](https://e2b.dev/docs/_next/static/media/node.ffbff9e8.svg)JavaScript & TypeScript

![](https://e2b.dev/docs/_next/static/media/python.c624d255.svg)Python

```python
import time

from e2b import Sandbox

watcher =None


defcreate_watcher(sandbox):  
# Start filesystem watcher for the /home directory
    watcher = sandbox.filesystem.watch_dir("/home")
    watcher.add_event_listener(lambdaevent: print(event))
    watcher.start()


sandbox =Sandbox(template="base")

create_watcher(sandbox)

# Create files in the /home directory inside the playground
# We'll receive notifications for these events through the watcher we created above.
for i inrange(10):
# `filesystem.write()` will trigger two events:
# 1. 'Create' when the file is created
# 2. 'Write' when the file is written to
    sandbox.filesystem.write(f"/home/file{i}.txt", f"Hello World {i}!")
    time.sleep(1)

sandbox.close()
```








# Starting process inside a sandbox

Here are the basic operations you can do with the process inside the sandbox:

* [Start process](https://e2b.dev/docs/sandbox/api/process#start-process)
* [Stop process](https://e2b.dev/docs/sandbox/api/process#stop-process)
* [Stdout](https://e2b.dev/docs/sandbox/api/process#stream-stdout)
* [Stdin](https://e2b.dev/docs/sandbox/api/process#send-stdin)
* [Stderr](https://e2b.dev/docs/sandbox/api/process#stream-stderr)
* [On exit](https://e2b.dev/docs/sandbox/api/process#on-process-exit)

## [Start process](https://e2b.dev/docs/sandbox/api/process#start-process)

![](https://e2b.dev/docs/_next/static/media/node.ffbff9e8.svg)JavaScript & TypeScript

![](https://e2b.dev/docs/_next/static/media/python.c624d255.svg)Python

```python
from e2b import Sandbox

sandbox =Sandbox(template="base")

npm_init = sandbox.process.start("npm init -y")
npm_init.wait()
print(npm_init.stdout)

sandbox.close()
```

Copy**Copied!**

## [Stop process](https://e2b.dev/docs/sandbox/api/process#stop-process)

![](https://e2b.dev/docs/_next/static/media/node.ffbff9e8.svg)JavaScript & TypeScript

![](https://e2b.dev/docs/_next/static/media/python.c624d255.svg)Python

```python
from e2b import Sandbox

sandbox =Sandbox(template="base")

npm_init = sandbox.process.start("npm init -y")
npm_init.kill()

# There will be no output because we immediately kill the `npm_init` process
print(npm_init.stdout)

sandbox.close()
```

Copy**Copied!**

## [Stream stdout](https://e2b.dev/docs/sandbox/api/process#stream-stdout)

Set either stdout handler for the whole sandbox level or per process.

![](https://e2b.dev/docs/_next/static/media/node.ffbff9e8.svg)JavaScript & TypeScript

![](https://e2b.dev/docs/_next/static/media/python.c624d255.svg)Python

```python
from e2b import Sandbox

sandbox =Sandbox(
    template="base",
    on_stdout=lambdaoutput: print("sandbox", output.line),  
)

proc = sandbox.process.start('echo "Hello World!"')
proc.wait()
# output: sandbox Hello World!

proc_with_custom_handler = sandbox.process.start(
'echo "Hello World!"',
    on_stdout=lambdaoutput: print("process", output.line),  
)
proc_with_custom_handler.wait()
# output: process Hello World!

sandbox.close()
```

Copy**Copied!**

## [Stream stderr](https://e2b.dev/docs/sandbox/api/process#stream-stderr)

Set either stderr handler for the whole sandbox level or per process.

![](https://e2b.dev/docs/_next/static/media/node.ffbff9e8.svg)JavaScript & TypeScript

![](https://e2b.dev/docs/_next/static/media/python.c624d255.svg)Python

```python
from e2b import Sandbox

sandbox =Sandbox(
    template="base",
    on_stderr=lambdaoutput: print("[sandbox]", output.line),  
)

# This command will fail and output to stderr because Golang isn't installed in the cloud playground
proc = sandbox.process.start("go version")
proc.wait()
# output: [sandbox] /bin/bash: line 1: go: command not found

proc_with_custom_handler = sandbox.process.start(
"go version",
    on_stderr=lambdaoutput: print("[process]", output.line),  
)
proc_with_custom_handler.wait()
# output: [process] /bin/bash: line 1: go: command not found

sandbox.close()
```

Copy**Copied!**

## [On process exit](https://e2b.dev/docs/sandbox/api/process#on-process-exit)

Set either on exit handler for the whole sandbox level or per process.

![](https://e2b.dev/docs/_next/static/media/node.ffbff9e8.svg)JavaScript & TypeScript

![](https://e2b.dev/docs/_next/static/media/python.c624d255.svg)Python

```python
from e2b import Sandbox

sandbox =Sandbox(
    template="base",
    on_exit=lambda: print("[sandbox]", "process ended"),  
)

proc = sandbox.process.start('echo "Hello World!"')
proc.wait()
# output: [sandbox] process ended

proc_with_custom_handler = sandbox.process.start(
'echo "Hello World!"',
    on_exit=lambda: print("[process]", "process ended"),  
)
proc_with_custom_handler.wait()
# output: [process] process ended

sandbox.close()
```

Copy**Copied!**

## [Send stdin](https://e2b.dev/docs/sandbox/api/process#send-stdin)

![](https://e2b.dev/docs/_next/static/media/node.ffbff9e8.svg)JavaScript & TypeScript

![](https://e2b.dev/docs/_next/static/media/python.c624d255.svg)Python

```python
from e2b import Sandbox

sandbox =Sandbox(template="base")

# This example will print back the string we send to the process using `send_stdin()`

proc = sandbox.process.start(
'while IFS= read -r line; do echo "$line"; sleep 1; done',
    on_stdout=print,
)
proc.send_stdin("AI Playground\n")
proc.kill()

sandbox.close()
```










# Current Working Directory

You can set a working directory either for the whole sandbox, a filesystem operation, or a new process.

## [Sandbox](https://e2b.dev/docs/sandbox/api/cwd#sandbox)

If the current working directory for the sandbox is not set, it will default to the home directory - `/home/user`.

![](https://e2b.dev/docs/_next/static/media/node.ffbff9e8.svg)JavaScript & TypeScript

![](https://e2b.dev/docs/_next/static/media/python.c624d255.svg)Python

```python
from e2b import Sandbox

sandbox =Sandbox(
    template="base",
    cwd="/code",  
)

# You can also change the cwd of an existing sandbox
sandbox.cwd ="/home"

sandbox.close()
```

Copy**Copied!**

## [Filesystem](https://e2b.dev/docs/sandbox/api/cwd#filesystem)

All filesystem operations with relative paths are relative to the current working directory.

![](https://e2b.dev/docs/_next/static/media/node.ffbff9e8.svg)JavaScript & TypeScript

![](https://e2b.dev/docs/_next/static/media/python.c624d255.svg)Python

```python
from e2b import Sandbox

sandbox =Sandbox(
    template="base",
    cwd="/home/user/code"
)
sandbox.filesystem.write("hello.txt", "Welcome to E2B!")
proc = sandbox.process.start("cat /home/user/code/hello.txt")
proc.wait()
print(proc.output.stdout)
# output: "Welcome to E2B!"

sandbox.filesystem.write("../hello.txt", "We hope you have a great day!")
proc2 = sandbox.process.start("cat /home/user/hello.txt")
proc2.wait()
print(proc2.output.stdout)
# output: "We hope you have a great day!"

sandbox.close()
```

Copy**Copied!**

## [Process](https://e2b.dev/docs/sandbox/api/cwd#process)

If you set a working directory for the sandbox, all processes will inherit it. You can override it for each process.

![](https://e2b.dev/docs/_next/static/media/node.ffbff9e8.svg)JavaScript & TypeScript

![](https://e2b.dev/docs/_next/static/media/python.c624d255.svg)Python

```python
from e2b import Sandbox

sandbox =Sandbox(template="base", cwd="/code")
sandbox_cwd = sandbox.process.start("pwd")
sandbox_cwd.wait()
print(sandbox_cwd.output.stdout)
# output: "/code"

process_cwd = sandbox.process.start("pwd", cwd="/home")
process_cwd.wait()
print(process_cwd.output.stdout)
# output: "/home"

sandbox.close()
```










# Sandbox URL

Each sandbox has its own URL that you can use to connect to any service running inside the sandbox.

For example, you can start a server inside the sandbox and connect to it from your browser.

![](https://e2b.dev/docs/_next/static/media/node.ffbff9e8.svg)JavaScript & TypeScript

![](https://e2b.dev/docs/_next/static/media/python.c624d255.svg)Python

```python
from e2b import Sandbox

sandbox =Sandbox(template="base")

url = sandbox.get_hostname()
print("https://"+ url)

sandbox.close()
```

Copy**Copied!**

If you want to get an URL for a specific port inside the sandbox, pass the port number to the `getHostname()`/`get_hostname()` method.

![](https://e2b.dev/docs/_next/static/media/node.ffbff9e8.svg)JavaScript & TypeScript

![](https://e2b.dev/docs/_next/static/media/python.c624d255.svg)Python

```python
from e2b import Sandbox

sandbox =Sandbox(template="base")

open_port =3000
url = sandbox.get_hostname(open_port)
print("https://"+ url)

sandbox.close()
```









# Timeouts

The SDK has a number of timeouts that can be configured to control how long the SDK will wait for a response from the E2B servers. **The default is 60 seconds.**

## [Timeout creating sandbox](https://e2b.dev/docs/sandbox/api/timeouts#timeout-creating-sandbox)

![](https://e2b.dev/docs/_next/static/media/node.ffbff9e8.svg)JavaScript & TypeScript

![](https://e2b.dev/docs/_next/static/media/python.c624d255.svg)Python

```python
from e2b import Sandbox

# Timeout 3s for the sandbox to open
sandbox =Sandbox(template="base", timeout=3)

sandbox.close()
```

Copy**Copied!**

## [Timeout process](https://e2b.dev/docs/sandbox/api/timeouts#timeout-process)

![](https://e2b.dev/docs/_next/static/media/node.ffbff9e8.svg)JavaScript & TypeScript

![](https://e2b.dev/docs/_next/static/media/python.c624d255.svg)Python

```python
from e2b import Sandbox

sandbox =Sandbox(template="base")

# Timeout 3s for the process to start
npm_init = sandbox.process.start("npm init -y", timeout=3)
npm_init.wait()

sandbox.close()
```

Copy**Copied!**

## [Timeout filesystem operations](https://e2b.dev/docs/sandbox/api/timeouts#timeout-filesystem-operations)

![](https://e2b.dev/docs/_next/static/media/node.ffbff9e8.svg)JavaScript & TypeScript

![](https://e2b.dev/docs/_next/static/media/python.c624d255.svg)Python

```python
from e2b import Sandbox

sandbox =Sandbox(template="base")

# Timeout 3s for the write operation
sandbox.filesystem.write("test.txt", "Hello World", timeout=3)

# Timeout 3s for the list operation
dir_content = sandbox.filesystem.list(".", timeout=3)
print(dir_content)

# Timeout 3s for the read operation
file_content = sandbox.filesystem.read("test.txt", timeout=3)
print(file_content)

sandbox.close()
```








# Connect to running sandbox

Disconnect and reconnect later to the same sandbox while keeping it alive

## [Description](https://e2b.dev/docs/sandbox/api/reconnect#description)

The sandboxes are by default kept alive only when connected to them. When you disconnect from a sandbox, it will be destroyed.

If you want to keep the sandbox alive even after disconnecting from it, you can explicitly say for how long you want to keep it alive. You can then disconnect from the sandbox and reconnect to it later. This can be useful for example in a **serverless environment** or  **chatbot application** .

The duration limit to keep the sandbox alive is 1 hour. If you need more, feel free to [reach out to us](https://e2b.dev/docs/getting-help) with your use.

## [Keep sandbox alive](https://e2b.dev/docs/sandbox/api/reconnect#keep-sandbox-alive)

The example below shows how to disconnect from a running sandbox and reconnect to it again while keeping the sandbox alive.

![](https://e2b.dev/docs/_next/static/media/node.ffbff9e8.svg)JavaScript & TypeScript

![](https://e2b.dev/docs/_next/static/media/python.c624d255.svg)Python

```python
import time
from e2b import Sandbox


sandbox =Sandbox('base')
```

Copy**Copied!**

Call the `keep_alive`/`keepAlive` method on the sandbox instance to keep it alive. You can specify the preferred duration, as a multiple of a default time unit, which is

* 1ms in JS
* 1s in Python.

You then disconnect from the sandbox.

![](https://e2b.dev/docs/_next/static/media/node.ffbff9e8.svg)JavaScript & TypeScript

![](https://e2b.dev/docs/_next/static/media/python.c624d255.svg)Python

```python
# Do something in the sandbox
sandbox.filesystem.write('hello.txt', 'Hello World!')

# Get the sandbox ID, we'll need it later
sandboxID = sandbox.id

# Keep the sandbox alive for 2 minutes
sandbox.keep_alive(60*60)

# Close the sandbox. Even if we close the sandbox, it will stay alive, because we explicitly called keep_alive().
sandbox.close()

# Do something else...
time.sleep(60)
```

Copy**Copied!**

You can then reconnect to the sandbox from anywhere.

![](https://e2b.dev/docs/_next/static/media/node.ffbff9e8.svg)JavaScript & TypeScript

![](https://e2b.dev/docs/_next/static/media/python.c624d255.svg)Python

```python
# Reconnect to the sandbox
sandbox2 = Sandbox.reconnect(sandboxID)

# Continue in using the sandbox
content = sandbox2.filesystem.read('hello.txt')
print(content)

# Close the sandbox
sandbox2.close()
```

Copy**Copied!**

## [Use sandbox metadata](https://e2b.dev/docs/sandbox/api/reconnect#use-sandbox-metadata)

Sandbox metadata can be very useful to store information about the sandbox. You can use it to store the user ID or any other information you need to keep track of and then use this info for reconnecting to the sandbox. You can read more about sandbox metadata [here](https://e2b.dev/docs/sandbox/api/metadata).
