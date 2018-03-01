from hashcode import Parser


def main():
    for name in ['d_metropolis.in']:
        Parser.parse(name)
        Parser.output('out_{}.out'.format(name))


if __name__ == "__main__":
    main()
