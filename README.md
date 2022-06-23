<p align="left">
  <img
    src="https://raftt-resources.s3.eu-central-1.amazonaws.com/docs/Logos/Navbar/logo-light.svg"
    srcDark="https://raftt-resources.s3.eu-central-1.amazonaws.com/docs/Logos/Navbar/logo-dark.svg"
    alt="TooDoo Screenshot"
  />
</p>

---

Checkout the raftt quickstart here: https://docs.raftt.io/docs/basics/tutorial

---

# Tutorial Using Our Sample To-Do App

We created [TooDoo](https://github.com/rafttio/toodoo), a simple to-do application, as a sample project to help you onboard Raftt quickly, without using your code.

The project is mainly written in Python (Flask) with some Go, but familiarity with these languages isn't necessary to complete this tutorial.

## Your First `raftt up`

In this section, we'll get you up and running with your very own Raftt environment and explain what happens under the hood.
Take the following steps -

1. Clone the project's repo - `git clone https://github.com/rafttio/toodoo`
2. `cd` into the repo's folder.
3. Run `raftt up` and wait for `Environment is ready!` to be printed.
    1. You will be prompted to log in with your GitHub account.
    2. Please note that building and deploying the images might take a minute or two.
4. Run `raftt status` to see the status of the environment services.

<p align="center">
  <img
    src="https://raftt-resources.s3.eu-central-1.amazonaws.com/docs/tutorial/status_main.png"
    alt="raftt status output"
  />
</p>

As seen in the above screenshot, the open port of the web container is [mapped](https://docs.raftt.io/docs/concepts/port_map) to the local port 3000. Let's see what happens when you [browse it](http://localhost:3000/).

<p align="center">
  <img
    src="https://raftt-resources.s3.eu-central-1.amazonaws.com/docs/tutorial/TooDoo.png"
    alt="TooDoo Screenshot"
  />
</p>

You can now play around with the app - add, remove, and edit tasks as you wish.

### Under the Hood

When you ran `raftt up`, you successfully started a sequence of events -

1. Authentication with GitHub.
2. Raftt's configuration file, [raftt.yml](https://docs.raftt.io/docs/config/raftt.yml), is detected by the Raftt client.
    1. In this case, raftt.yml was cloned with the repo. It will automatically be generated with default values if it doesn't exist.
3. The raftt.yml file refers to the environment definitions - the docker-compose file and the [dev container](https://docs.raftt.io/docs/config/dev_container) definitions.
4. A new private and isolated environment is spawned in Raftt's cloud.

If you have docker installed, you can run `docker ps` and see that nothing runs on your machine - it's all remote!

## Working With the Env

Since your env is up, you can play around with the code and see how your changes affect the site!

### Changing the Color of a Button

In line 74 of the file `<repo>/templates/index.html`, change `btn-primary` to `btn-danger`, save, and reload the page. The submit button should now be colored red.

### Debugging the Application

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

One of the most common things devs do is to debug their environment.
Raftt currently supports interactively debugging Python and Go code using Visual Studio Code or any JetBrains IDE. Additional support is continuously being added.

<Tabs className="unique-tabs">
<TabItem value="vscode" label="VS Code" default>

To debug the application, follow these steps -

1. Open the project in VS Code.
2. Add a breakpoint inside the function `create` in the file `app.py`.
3. Start debugging using the debug configuration `web`.
    1. Debugging is pre-configured in this project by files committed in the repo. See [here](https://docs.raftt.io/docs/debugging/VSCode#configuration) for details on how to do it yourself.
4. Create a task in the TooDoo app.
5. Check if it stopped where you added the breakpoint.
6. Debug the remote service as if it were local.

</TabItem>
<TabItem value="jetbrains" label="JetBrains IDEs">

To debug the application, follow these steps -

1. Open the project in any JetBrains IDE.
2. Install Raftt's plugin according to the instructions [here](https://docs.raftt.io/docs/debugging/JetBrains#installing-the-plugin).
3. Add a breakpoint inside the function `create` in the file `app.py`.
4. Start debugging using the debug configuration `web`.
    1. Debugging is pre-configured in this project by files committed in the repo. See [here](https://docs.raftt.io/docs/debugging/JetBrains#configuration) for details on how to do it yourself.
    2. The IDE will ask you to configure a Python interpreter. You can ignore the request or choose an interpreter of your choice. It doesn't affect the remote environment that uses its own interpreter.
5. Create a task in the TooDoo app.
6. Check if it stopped where you added the breakpoint.
7. Debug the remote service as if it were local.

</TabItem>
</Tabs>

### Breaking the Code

You should now explore what happens if you make a mistake in the code. Make a change that will cause the main process to crash. You can go to `<repo>/app.py` and add `This won't work` to line 6. Flask auto-reload feature will automatically update the app, causing it to crash.
To "debug" the issue, you can run `raftt logs web` and see the error in the container logs.  
Now fix the issue you create - revert the breaking change and restart the app. You can restart it by running your code from the IDE (if you configured it in the [previous](#debugging-the-application) section) or run `raftt restart web` from the CLI which does the same. Note that it restarts the main process, while the container itself isn't reloaded. If you now refresh the webpage, you'll see the page loads successfully.  

### Branch Switching

Raftt seamlessly [integrates with your workflow](https://docs.raftt.io/docs/concepts/git_workflows) and makes switching between branches a breeze.  
Switching to a new branch spawned a new environment while the previous environment(s) are waiting - if you want to come back to them later.

Switch to a different branch using `git checkout v2` and refresh the page. Since a new env is spawned, it might take a minute or two until the env is responsive. The spawning happens in the background, if you want to follow the spawning status, you can run `raftt status -w`.

You can now see that this branch has several new features - choosing an emoji for each task and counting the number of active users connected to your amazing TooDoo app.
Note that the tasks have changed, both in content and in the database schema. With Raftt, this change is seamless.
In addition, if you run `raftt status`, you'll notice a few changes -

1. The environment now has two additional services - `redis` and `live-backend` (running Go).
2. Python in the `web` container changed seamlessly from v3.9 to v3.10 without requiring any dependency change on your side.

<p align="center">
  <img
    src="https://raftt-resources.s3.eu-central-1.amazonaws.com/docs/tutorial/status_v2.png"
    alt="raftt status output"
  />
</p>

You can go back to main using `git checkout main` and look at any changes you previously made to the task list remain. For the next tutorial stage, you'll want to be in the `v2` branch.

## Collaborating With Other Team Members

Suppose you want to share your magnificent work on the active users features with the PM that defined it. You're used to calling your PM to see it work on your machine, but she's WFH (working-from-home). So, you may share your screen using Slack, but wouldn't it be much easier if you could just give her direct access to your dev environment? Well, with Raftt you can!

Ensure you're in the right branch - which means you're connected to the right environment.
Then, just run `raftt expose web` and share the public URL!

## Try It With Your Project

After seeing how easy it is to work with Raftt, you're welcome to use raftt on any project of yours - open source or private.  
We'd love to hear about your experience in [our Slack community](https://join.slack.com/t/rafttcommunity/shared_invite/zt-196nlb5ra-rYPWEqQF~ETdgx9aqWANnw) or by [contacting us](https://raftt.io/contact-us) directly.

---
Built with ☕ by [raftt](!https://www.raftt.io)
