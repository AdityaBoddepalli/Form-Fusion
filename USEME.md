# Directions:

1. Clone the repository. I recommend using GitHub Desktop since it will automatically create a project folder
   for the repository under the GitHub folder.

2. Install the Anaconda package manager. Make sure you select the option to add it to PATH so you can use conda
   in the command line.

3. In the command line, create a new environment:

    conda create --name beanpot python==3.9.16

4. Navigate to the project folder where you cloned the repository. Run the following commands:

    conda activate beanpot

    pip install -r requirements.txt

5. Open the repository in VSCode. In the bottom right, ensure you are using the environment
   (you should see something like {'beanpot': conda})


6. Note: If you pull from the repository and run the flask app and an error occurred where a dependency
   wasn't recognized, re-run the command to install requirements.