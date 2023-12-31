.. |NAME| replace:: API Compose
.. |CLI_NAME| replace:: acp
.. |PACKAGE_NAME| replace:: api-compose


|NAME|
~~~~~~~~~~~~~~~~~~~~
.. image:: assets/logo.png
   :align: center
   :alt: Generated from Smashinglogo



.. image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/kenho811/api_compose.git/HEAD?labpath=tutorials




Tutorials
=====================

On Binder.org
----------------------

A tutorial series as jupyter notebook is uploaded to binder.org. Please free to try it out there first!

Link: https://mybinder.org/v2/gh/kenho811/api_compose.git/HEAD?labpath=tutorials

Local
----------------------

.. code-block::

   docker compose -f ./tutorials/docker-compose.yaml up


Installation
=====================

`PyPI Package <https://pypi.org/project/api-compose>`_

.. parsed-literal::

   pip install |PACKAGE_NAME|

Get Started
------------------

.. parsed-literal::

   # creates a sample project for you to build on
   |CLI_NAME| scaffold <your_project_name>

Run the programme
-------------------------

.. parsed-literal::

   |CLI_NAME| run

- Explore the CLI's capabilities by running `acp` or `acp --help`


Examples
============================
- Examples are in **./examples** folder

`API Examples <https://github.com/kenho811/api_compose/tree/main/examples>`_


Features
=====================

Declaration-based API Call Composition
--------------------------------------------------

- Allows API calls to be declared as Models.

- Distinguishes between **Compile Time Rendering** and **Run Time Rendering**

- Leverages networkx to determine the execution order of each API call.

- Exposes decorator **@FunctionsRegistry** to for users to register user-defined jinja functions (Globals, Filters and Tests)


Useful Builtin Jinja Globals
----------------------------------------

Builtin Jinja Globals allow users to specify which part (e.g. headers, body etc.) of an API action (e.g. login, get_images etc.) to use.

.. code-block::

    ## Get the value of the field field_one of the returned body from the login_action API call
    {{ action('login_action')| output_body| jpath('$.field_one') }}

    ## Get the value of the field field_one of the input headers from the login_action API call
    {{ action('login_action')| input_headers | jpath('$.field_one') }}

    ## Get the rendered body of the current API call
    {{ action('self')| config_body }}

Supported API Calls Type - Adapters
----------------------------------------

- Below is the table which breaks down the type of API Call by

    - Protocol (Column)
    - Data Format (Row)


.. table::

    +------+------+-----------+-----+
    |      | HTTP | WebSocket | FIX |
    +======+======+===========+=====+
    | json | True | WIP       | TBD |
    +------+------+-----------+-----+
    | xml  | True | TBD       | TBD |
    +------+------+-----------+-----+

- WIP means Working in Progress. It means it is being worked on now.

- TBD means to be determined.  It means it will be planned in the future.


Schema Validation
---------------------------
- Leverages **jsonschema** and **xmlschema** to validate returned json and xml data respectively.

Assertion
---------------------------

- Allows users to use Jinja to make assertions between API Calls Result

.. code-block::

    # assert that value of a the field 'field_one' in the output body of action 'action_one' equals 1
    {{ action('action_one')| output_body| jpath('$.field_one') == 1 }}

    # assert that value of a the field 'field_one' in the output body of action 'action_one' equals 'a'
    {{ action('action_two')| output_body| xpath('/field_one/text()') == 'a' }}


Reporting
---------------------------

- Presents Test Results nicely in HTML reports



Architectural Diagram
===========================

.. figure:: ./assets/framework_architecture.png
   :scale: 70%
   :align: center
   :alt: API Compose Framwork Architecture

   The above is the Programme Architecture.

   Lucid Chart here: `https://lucid.app/lucidchart/f8d1f9f9-bc93-46ec-8e4f-6561a4c822c3/edit?beaconFlowId=70D4EDD3B7971E6C&invitationId=inv_c7b45baf-050c-480b-923e-2979440ce4c8&page=0_0#`


.. figure:: ./assets/framework_building_blocks.png

    Hierarchical structure of the models

    Lucid Chart here: https://lucid.app/lucidchart/f8d1f9f9-bc93-46ec-8e4f-6561a4c822c3/edit?beaconFlowId=70D4EDD3B7971E6C&invitationId=inv_c7b45baf-050c-480b-923e-2979440ce4c8&page=p0OVapsRWlkY#



Jinja Templating
============================

Compile Time Rendering
--------------------------------

- To make templates reusable, the programme exposes the means to render template files using the below syntax:

.. code-block::

    block_start_string='[%'
    block_end_string='%]'
    variable_start_string='[['
    variable_end_string=']]'
    comment_start_string='[#'
    comment_end_string='#]'

Run Time Rendering
--------------------------------

- To allow for inter-API Call dependencies within a given scenario, the programme also exposes the means to render templated fields using the below syntax:

.. code-block::

    block_start_string='{%'
    block_end_string='%}'
    variable_start_string='{{'
    variable_end_string='}}'
    comment_start_string='{#'
    comment_end_string='#}'