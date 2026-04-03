# Student 1: Agilan Kumar
# Spire Id: 35073172
#
# Student 2: Adam Nativ
# Spire Id: 35141601

from course_management import CourseItem, Course, CourseManager, DEFAULT_WEIGHTS


def display_menu():
    print("\nCourse Management System")
    print("1.  Add a new course")
    print("2.  View all courses")
    print("3.  Add an item to a course")
    print("4.  View all items in a course")
    print("5.  Mark an item as completed")
    print("6.  Update an item's score")
    print("7.  View pending items")
    print("8.  Calculate course grade")
    print("9.  Customize category weights")
    print("10. Exit")


def prompt_course_code(manager):
    """
    Display all current courses, then prompt the user to enter a course code.

    Steps:
        1. Print a header: "Current courses:"
        2. Print each string returned by manager.display_courses(), indented with "  ".
        3. Prompt: "Enter course code: "
        4. Call manager.find_course_by_code() with the entered code.
        5. If not found, print "Course not found." and return None.
        6. Return the matching Course object.

    Parameters:
        manager (CourseManager): The active course manager.

    Returns:
        Course or None.
    """
    print("Current courses:")
    for course in manager.display_courses():
        print("  " + course)
    code = input("Enter course code: ")
    course = manager.find_course_by_code(code)
    if course is None:
        print("Course not found.")
        return None
    return course


def main():
    manager = CourseManager()

    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            # Create a Course object and add it to manager via manager.add_course()
            # Print "Course added successfully."
            name = input("Enter course name: ").strip()
            code = input("Enter course code: ").strip()
            instructor = input("Enter instructor name: ").strip()
            manager.add_course(Course(name, code, instructor))
            print("Course added successfully.")

        elif choice == "2":
            for course in manager.display_courses():
                print(course)

        elif choice == "3":
            # TODO: Call prompt_course_code(manager) to get the course
            # If None, use 'continue' to go back to the menu
            # Otherwise, prompt for item title, category, due date, and points possible
            # Create a CourseItem and add it to the course via course.add_item()
            # Print "Item added successfully."
            course = prompt_course_code(manager)
            if course is None:
                continue
            title = input("Enter course title: ")
            category = input("Enter category: ")
            due_date = input("Enter due date: ")
            points_possible = float(input("Enter points possible: "))
            course.add_item(CourseItem(title, category, due_date, points_possible))
            print("Item added successfully.")

        elif choice == "4":
            # TODO: Call prompt_course_code(manager) to get the course
            # If None, use 'continue'
            # Otherwise, print each string returned by course.display_items()
            course = prompt_course_code(manager)
            if course is None:
                continue
            for i in course.display_items():
                print(i)

        elif choice == "5":
            # TODO: Call prompt_course_code(manager) to get the course
            # If None, use 'continue'
            # Prompt for item title, call course.find_item()
            # If None, print "Item not found."
            # Otherwise, call item.mark_complete() and print "Item marked as completed."
            course = prompt_course_code(manager)
            if course is None:
                continue
            item = course.find_item(input("Enter item title: "))
            if item is None:
                print("Item not found.")
            else:
                item.mark_complete()
                print("Item marked as completed.")

        elif choice == "6":
            # TODO: Call prompt_course_code(manager) to get the course
            # If None, use 'continue'
            # Prompt for item title, call course.find_item()
            # If None, print "Item not found."
            # Otherwise, prompt for score (float), call item.update_score()
            # Print "Score updated successfully."
            course = prompt_course_code(manager)
            if course is None:
                continue
            item = course.find_item(input("Enter item title: "))
            if item is None:
                print("Item not found.")
            else:
                score = float(input("Enter score: "))
                item.update_score(score)
                print("Score updated successfully.")

        elif choice == "7":
            # TODO: Call prompt_course_code(manager) to get the course
            # If None, use 'continue'
            # Print each string returned by course.display_pending_items()
            course = prompt_course_code(manager)
            if course is None:
                continue
            for item in course.display_pending_items():
                print(item)

        elif choice == "8":
            # TODO: Call prompt_course_code(manager) to get the course
            # If None, use 'continue'
            # Call course.calculate_grade()
            # If None, print "No graded items yet."
            # Otherwise:
            #   Print "Course Grade for <course_code>: <course_name>"
            #   Print "  Weighted average : <percentage:.2f>%"
            #   Print "  Letter grade     : <letter>"
            #   Print a per-category breakdown (see project spec for format)
            course = prompt_course_code(manager)
            if course is None:
                continue
            grade_info = course.calculate_grade()
            if grade_info is None:
                print("No graded items yet.")
            else:
                percentage, letter = grade_info
                print(f"\nCourse Grade for {course.course_code}: {course.course_name}")
                print(f"  Weighted average : {percentage:.2f}%")
                print(f"  Letter grade     : {letter}")

                print("\nCategory breakdown:")
                for category, weight in course.weights.items():
                    graded = []
                    for item in course.items:
                        if item.category == category and item.points_earned is not None:
                            graded.append(item)
                    if not graded:
                        print(f"  {category} ({weight}%): No graded items")
                    else:
                        total_earned = 0
                        total_possible = 0
                        for item in graded:
                            total_earned += item.points_earned
                            total_possible += item.points_possible

                        category_pct = (total_earned / total_possible) * 100

                        print(f"  {category} ({weight}%): {total_earned}/{total_possible} = {category_pct:.1f}%")

        elif choice == "9":
            # TODO: Call prompt_course_code(manager) to get the course
            # If None, use 'continue'
            # Print "Current weights for <course_code>:"
            # Print each string from course.display_weights()
            # Print instructions, then prompt the user for a new weight per category
            #   (pressing Enter keeps the current value)
            # Validate that the new weights sum to ~100
            # If valid, call course.set_weights() and print "Weights updated successfully."
            # If invalid, print "Weights must sum to 100 (got <total:.2f>). No changes made."
            course = prompt_course_code(manager)
            if course is None:
                continue
            print(f"Current weights for {course.course_code}:")
            for weight_line in course.display_weights():
                print(weight_line)
            print("Enter new weights for each category (must sum to 100). Press Enter to keep current value.")
            new_weights = {}
            for category in course.weights:
                user_input = input(f"  {category} (currently {course.weights[category]}%): ")
                if user_input:
                    new_weights[category] = float(user_input)
                else:
                    new_weights[category] = course.weights[category]
            total = sum(new_weights.values())
            if abs(total - 100.0) < 0.01:
                course.set_weights(new_weights)
                print("Weights updated successfully.")
            else:
                print(f"Weights must sum to 100 (got {total:.2f}). No changes made.")

        elif choice == "10":
            # TODO: Print "Exiting program." and break out of the loop
            print("Exiting program.")
            break

        else:
            # TODO: Print "Invalid choice. Please try again."
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
