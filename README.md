# Novel-Analysis
This project is capable of analyzing the entire text of a *[Project Gutenberg](https://www.gutenberg.org/)* Novel and determine the frequency of the top *n* words in the novel. It will also extract the metadata of the novel (i.e. Title, Author, Language, etc...).


## Before Running
Make sure to initialize a virtual environment before installing the packages in `requirements.txt`.

#### **How to use a virtual environment:**
For ease of use you can use the virtual environment Python already comes packaged with `venv`.

- Open your terminal or command prompt.
- Navigate to your project directory using the `cd` command.
- Run the following command to create a virtual environment name "myenv" (you can use any name):
  - `python -m venv myenv`
- Activate the virtual environment:
   - On macOS / Linux:
   `source myenv/bin/actiavte`
   - On Windows:
   `myenv\Scrips\activate`

#### **Installing the packages after creating a virtual environment:**

After creating the virtual environment and activating it. Run the following command to install the packages in the requirements.txt file: `pip install -r /path/to/requirements.txt`.