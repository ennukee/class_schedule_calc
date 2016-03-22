# Classbuddy

(because I like naming all my scripts with 'buddy')

This script is designed to take in a series of comma-separated values consisting of a class name, credit worth, and strictly formatted time range strings.

### Requirements

 * Python 3.5+ (functionality on lower versions not guaranteed)
 * A CSV file with your tentative class information
 * **Recommended**: Google Calendar access (to view CSV outputs visually)

## How to use

#### Downloading the source

Pretty simple. Hit the 'Download ZIP' button on the upper right of the file list (just above the top right corner) to download a compressed version of the source code. Unzip it and continue on with the instructions.

#### Your CSV file

The important part is to make sure your CSV file is set up properly. It will break very easily (and it will tell you so) if you improperly write the data in your CSV file. You can name it whatever you like, but make sure to supply this file name to the script later on.

Important things to note:

 * First and foremost, take a look at `test.csv` [here](https://github.com/enragednuke/class_schedule_calc/blob/master/test.csv). It will make everything much easier to understand.
 * Each row follows the format `CLASS NAME,CREDIT COUNT,TIME1,TIME2,etc`
 * Leave no whitespace around the commas
 * Do not include blank lines at the end of your file
 * You can have spaces in your class name as long as the space is not next to the comma
 * Credit count **must be an integer value**. Do not try typing "four" or "five" or use other languages. It will not work.
 * The form for the time slots are `DAYS_OF_WEEK hh:mm-hh:mm`. If you've seen/used my [time_overlap_calc](https://github.com/enragednuke/time_overlap_calc) code, it is very similarly formatted. The first set of `hh:mm` is the start time, the second is the end time. Simple.
 * `DAYS_OF_WEEK` is a concatenated string of any number of these five values: `Mo`, `Tu`, `We`, `Th`, or `Fr`. It does not support weekend classes, nor should you try to extend the abbreviations more than I have written. So, if your class is on Monday, Wednesday, and Friday, you would put `MoWeFr` for the `DAYS_OF_WEEK` portion. See the `test.csv` file for some examples.

Some tips for writing/managing your CSV:

 * You can write out every class you MAY possible take and then filter out specific ones as you re-run the script multiple times. This can be done by adding a `!INC` to any part of that row (note, make sure it hugs the commas like everything else, consider it like a column in a table). 
 * Make extra lines that start with `!INC` (but still have the class name) to hold timings you don't want to go to, but still want to hold on to incase it's necessary to make a viable schedule.
 * See `test.csv` for examples of this in action

#### Running the script

Like my other scripts, you just need to run the python file from the command line. You will need to supply it with the relative path to a CSV file. I have provided an example `test.csv` file in the repository. To use the program with that CSV, you would type this:

```
> python class_schedule_finder.py test.csv
```

If you have both Python 2.\* and Python 3.\* installed, you may need to use the following command instead if you have not done an `alias python='python3'`:

```
> python3 class_schedule_finder.py test.csv
```

It will display the results of parsing your CSV file and ask you if it looks okay. Scan it and make sure nothing got parsed incorrectly (by your or my error, if it's the latter please submit an issue!).

It will then calculate all possible arrangements of your schedule. Be wary that if the classes are very loosely spread, you could end up with a **lot** of CSV files in your output. As the program suggests, try to remove the timings you dislike for certain classes to try and re-calculate more favorable scheduled.

Once you've reduced it to 1-2 schedules, you should try importing them to **Google Calendar** or a **spreadsheet software** (Google Sheets, Excel, etc) to view them graphically. I personally recommend Google Calendar, as it provides the best visual of the options available.
