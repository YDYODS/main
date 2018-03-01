from hashcode import Parser


def main():
    for name in ['a_example.in', 'b_should_be_easy.in', 'c_no_hurry.in', 'd_metropolis.in', 'e_high_bonus.in']:
        Parser.parse(name)
        Parser.output('out_{}.out'.format(name))


if __name__ == "__main__":
    main()
