from hw1 import find_by_author, find_by_tag, find_by_tags


def main():
    check_loop_status = True
    while check_loop_status:
        user_input = input("Input command ([name: Author name] or [tag:life] or Exit): ")
        check_conditions = user_input.strip().split(':', 1)
        if user_input.lower() == "exit":
            print("Good by!")
            check_loop_status = False
        elif check_conditions[0].startswith("name"):
            normalize_author = check_conditions[1].strip()
            print(find_by_author(normalize_author))
        elif check_conditions[0] == "tag":
            normalize_tag = check_conditions[1].strip()
            print(find_by_tag(normalize_tag))
        elif check_conditions[0] == "tags":
            normalize_tags = check_conditions[1].strip().split(',')
            print(find_by_tags(normalize_tags))


if __name__ == '__main__':
    main()
