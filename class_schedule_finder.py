import os, sys, csv, time, re, random, string
import datetime
import textwrap
from collections import defaultdict
import itertools

class Cluster:
  def __init__(self, name, cluster):
    self.name = name
    self.cluster = cluster

  def __str__(self):
    s = "  {} cluster\n".format(self.name)
    for c in self.cluster:
      s += str(c) + "\n"
    return s

class Class:
  def __init__(self, name, ranges):
    self.name = name
    self.ranges = ranges

  def __str__(self):
    s = "{}\n".format(self.name)
    for r in self.ranges:
      s += str(r) + "\n"
    return s

  def overlaps_with(self, other):
    for i in self.ranges:
      for q in other.ranges:
        if i.overlaps_with(q):
          return True
    return False

class TimeRange:
  def __init__(self, name, start, end):
    self.name = name
    self.start = start
    self.end = end

  def __str__(self):
    return "{}: {} - {}".format(self.name, stylize_time(self.start.time()), stylize_time(self.end.time()))

  def overlaps_with(self, other):
    latest_start = max(other.start, self.start)
    earliest_end = min(other.end, self.end)
    overlap = earliest_end - latest_start
    if overlap > datetime.timedelta(0):
      return True
    else:
      return False

def main(lines, cr_t):
  timeranges = {}
  valid_schedules = 0

  print('Gathering data from CSV file...\n')
  for line in lines:
    cluster = []
    for d in lines[line]:
      cluster.append(Class(line, generate_times(d)))
    timeranges[line] = Cluster(line, cluster)

  for name, cluster in timeranges.items():
    print(cluster)

  print('Please look over the above times and confirm that these are correct\n')
  d = input('Type \'yes\' if these are right: ')
  if 'yes' not in d:
    print('Closing program... please go correct the CSV file')
    sys.exit()

  print('Removing all old output files...\n')
  for fp in os.listdir('./output'):
    os.remove('./output/'+fp)
  for setc in itertools.product(*[x[1].cluster for x in timeranges.items()]):
    is_valid = True 
    for s1, s2 in itertools.combinations(setc, 2):
      if s1.overlaps_with(s2):
        is_valid = False
    if is_valid:
      valid_schedules += 1
      print('Found a valid schedule setup...')
      print('Beginning outputting of a proper schedule to CSV...')
      r_str = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
      with open('output/CP_output_{}.csv'.format(r_str), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Subject","Start Date","Start Time", "End Date", "End Time", "All Day Event","Description","Location","Private"])
        for cl in setc:
          for tr in cl.ranges:
            now = datetime.datetime.now()
            weekday = now.weekday()
            offset = day_to_int(tr.name) - weekday
            the_day = (now + datetime.timedelta(offset, 0)).strftime("%D")

            # Format: name, start_day, start_time, end_day, end_time, all_day_event (bool), description, location, private
            writer.writerow([cl.name, the_day, stylize_time(tr.start.time()), the_day, stylize_time(tr.end.time()), False, '', '', False])
      print('Done outputting data to CSV for proper schedule\n')

  output = """\
    -----------------------------------

    Done! Please see the output folder for your CSVs. Upload them to Google Calendar to see what it would look like. Alternatively, you can preview it using a spreadsheet software aswell

    Total credit count: {}
    You have {} possible schedules with the provided classes. {}

    Fun fact: You can put !INC anywhere in a row (though it can be the only thing in said column) to completely prevent the program from reading it. Use this to leave out time slots you dislike
    
    -----------------------------------
    """.format(cr_t, valid_schedules, 'Please consider removing time frames you dislke from the CSV file to reduce this =D' if valid_schedules > 1 else "")
  if valid_schedules > 0:
    print(textwrap.dedent(output))
  else:
    print('The program could not find any valid schedules. Sorry.')

def generate_times(i):
  sd, sd2 = split_days(i)
  st = [split_times(x) for x in sd]
  ct = [(converted_time(x[0]), converted_time(x[1])) for x in st]
  tr = [TimeRange(sd2[ct.index(x)], x[0], x[1]) for x in ct]
  return tr
  
def split_days(i):
  """ For strings of form 'Day+ hh:mm-hh:mm"""
  s = i.split()
  days = re.findall('[A-Z][^A-Z]*', s[0])
  return (list(map(lambda x: '{} {}'.format(x, s[1]), days)), days)

def split_times(i):
  """ For strings of form 'Day hh:mm-hh:mm' """
  split_str = i.split()
  times = split_str[1].split('-')
  return list(map(lambda s: "{} {}".format(split_str[0], s), times))

def converted_time(i):
  """ For strings of the form Day hh:mm"""
  split_str = i.split()
  times = datetime.datetime( *(time.strptime(split_str[1], "%H:%M")[:6]) ) + datetime.timedelta(day_to_int(split_str[0])) 
  return times

def stylize_time(i):
  """ Convert time objects to a better public-facing form """
  return i.strftime('%I:%M %p')

def day_to_int(i):
  try:
    return {'Mo': 0, 'Tu': 1, 'We': 2, 'Th': 3, 'Fr': 4}[i]
  except Exception as e:
    return -1

if __name__ == '__main__':
  if len(sys.argv) is not 2:
    print('Please supply a CSV file path in quotations (like this: \"data/file.csv\")')

  elif sys.argv[1][-4:] != '.csv':
    print('Please supply a CSV file! (given: \'{}\')'.format(sys.argv[1][-4:]))

  else:
    try:
      credit_total = 0
      with open(sys.argv[1], 'r') as fp:
        dic = {}
        for row in csv.reader(fp):
          if row and not '!INC' in row:
            dic[row[0]] = row[2:]
            credit_total += int(row[1])
        main(dic, credit_total)
    except IOError as e:
      print('Invalid filepath provided (given: \'{}\')'.format(sys.argv[1]))
    except ValueError as e:
      print('Make sure the second column of your CSV file is the credit value for each class')
    except Exception as e:
      print('Something went wrong during the loading of your file')
      print('{}: {}'.format(type(e).__name__, e))