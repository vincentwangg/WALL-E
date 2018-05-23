import argparse
from ostracod_detection.locating.gen_temporal_ostracods import gen_ostracods
from ostracod_detection.matching.match_temporal import get_ostracod_matches

def main():
  parser = argparse.ArgumentParser(description='Find Ostracod Matches')
  parser.add_argument('l_feed', type=str, help='file name of left feed')
  parser.add_argument('r_feed', type=str, help='file name of right feed')

  args = parser.parse_args()

  ostracods_l = gen_ostracods(args.l_feed)
  ostracods_r = gen_ostracods(args.r_feed)

  print(get_ostracod_matches(ostracods_l, ostracods_r))

if __name__ == '__main__':
    main()