class CourseItem:
    def __init__(self, title, category, due_date, points_possible):
        """
        Initialize a CourseItem with the given attributes.

        Parameters:
            title (str): The name of the item (e.g., "HW1", "Quiz 1").
            category (str): The type of item (e.g., "Homework", "Quiz", "Exam", "Lecture Note").
            due_date (str): The due date as a string (e.g., "2026-03-20").
            points_possible (float): The maximum points for this item.

        Instance variables to set:
            self.title          -- the item title
            self.category       -- the item category
            self.due_date       -- the due date string
            self.points_possible -- max points for this item
            self.points_earned  -- starts as None (not yet graded)
            self.completed      -- starts as False
        """
        # TODO: Set all instance variables described above
        pass

    def mark_complete(self):
        """
        Mark this item as completed.

        Rules:
            - Sets self.completed to True.
            - Must not print anything.
        """
        # TODO: Implement this method
        pass

    def update_score(self, score):
        """
        Record the score earned on this item.

        Parameters:
            score (float): The points earned to assign to self.points_earned.

        Rules:
            - Must not print anything.
        """
        self.points_earned = score

    def display_info(self):
        """
        Return a formatted string describing this item.

        Format:
            "<category>: <title> | Due: <due_date> | Score: <score_text> | Status: <status>"

        Where:
            score_text is "Not graded" if points_earned is None,
                        otherwise "<points_earned>/<points_possible>"
            status is "Completed" if completed is True, otherwise "Incomplete"

        Returns:
            str: The formatted item info string.
        """
        if self.points_earned is None:
            score_text = "Not graded"
        else:
            score_text = f"{self.points_earned}/{self.points_possible}"

        if self.completed:
            status = "Completed"
        else:
            status = "Incomplete"

        return f"{self.category}: {self.title} | Due: {self.due_date} | Score: {score_text} | Status: {status}"


# Default category weights — must sum to 100.
# Each Course gets its own copy of these weights, which can be customized.
DEFAULT_WEIGHTS = {
    "Homework":     20.0,
    "Quiz":         10.0,
    "Exam":         30.0,
    "Lecture Note": 5.0,
    "Project":      35.0,
}


def score_to_letter(percentage):
    """
    Convert a numeric percentage to a US university letter grade.

    Standard scale:
        A  >= 93   A- >= 90
        B+ >= 87   B  >= 83   B- >= 80
        C+ >= 77   C  >= 73   C- >= 70
        D+ >= 67   D  >= 63   D- >= 60
        F  <  60

    Parameters:
        percentage (float): Grade percentage (0–100).

    Returns:
        str: The corresponding letter grade string (e.g., "A", "B+", "C-").
    """
    # TODO: Implement the letter grade scale above using if/elif/else
    pass


class Course:
    def __init__(self, course_name, course_code, instructor_name):
        """
        Initialize a Course.

        Parameters:
            course_name (str): Full name of the course (e.g., "Intro to Python").
            course_code (str): Course code (e.g., "ECE122").
            instructor_name (str): Name of the instructor.

        Instance variables to set:
            self.course_name     -- full course name
            self.course_code     -- course code
            self.instructor_name -- instructor name
            self.items           -- empty list (will hold CourseItem objects)
            self.weights         -- a copy of DEFAULT_WEIGHTS (use dict() to copy)
        """
        self.course_name = course_name
        self.course_code = course_code
        self.instructor_name = instructor_name
        self.items = []
        self.weights = dict(DEFAULT_WEIGHTS)

    # ── Weight management ─────────────────────────────────────────────────

    def set_weights(self, new_weights):
        """
        Replace this course's category weights with new_weights.

        Parameters:
            new_weights (dict): Mapping of category name -> percentage weight.
                                Values must sum to 100 (within 0.01 tolerance).

        Returns:
            bool: True if weights were successfully set,
                  False if they do not sum to ~100.

        Rules:
            - Must not print anything.
        """
        # TODO: Check that the values sum to ~100, then update self.weights
        pass

    def display_weights(self):
        """
        Return a list of formatted strings showing the current category weights.

        Format for each entry:
            "  <category>: <weight>%"

        Returns:
            list[str]: One string per category in self.weights.
        """
        # TODO: Build and return the list of weight strings
        pass

    # ── Item management ───────────────────────────────────────────────────

    def add_item(self, item):
        """
        Add a CourseItem to this course's items list.

        Parameters:
            item (CourseItem): The item to add.

        Rules:
            - Must not print anything.
        """
        # TODO: Append item to self.items
        pass

    def remove_item(self, item_title):
        """
        Remove an item from this course by title (case-insensitive).

        Parameters:
            item_title (str): Title of the item to remove.

        Returns:
            bool: True if the item was found and removed, False otherwise.

        Rules:
            - Comparison must be case-insensitive.
            - Must not print anything.
        """
        # TODO: Loop through self.items, find the match, remove it, return True
        # If not found, return False
        pass

    def find_item(self, item_title):
        """
        Find and return a CourseItem by title (case-insensitive).

        Parameters:
            item_title (str): Title to search for.

        Returns:
            CourseItem: The matching item, or None if not found.

        Rules:
            - Comparison must be case-insensitive.
            - Must not print anything.
        """
        # TODO: Loop through self.items and return the matching item or None
        pass

    def display_items(self):
        """
        Return a list of formatted strings for all items in this course.

        Returns:
            list[str]: One string per item from display_info(),
                       or ["No items found."] if the course has no items.
        """
        # TODO: Implement this method
        pass

    def display_pending_items(self):
        """
        Return a list of formatted strings for all incomplete items.

        Returns:
            list[str]: Strings from display_info() for items where completed is False,
                       or ["No pending items."] if all items are complete.
        """
        # TODO: Filter items where completed == False and return their display_info() strings
        pass

    # ── Grade calculation ─────────────────────────────────────────────────

    def calculate_grade(self):
        """
        Calculate the weighted overall grade for this course.

        Algorithm:
            For each category in self.weights that has weight > 0:
              1. Collect all graded items in that category
                 (items where points_earned is not None).
              2. If none exist, skip this category entirely.
              3. Compute category_pct = sum(points_earned) / sum(points_possible) * 100.
              4. Add category_pct * weight to a running weighted_sum.
              5. Add weight to a running active_weight.
            Final percentage = weighted_sum / active_weight.

        Returns:
            tuple(float, str) or None:
                A tuple of (percentage rounded to 2 decimal places, letter grade string)
                if at least one item has been graded.
                None if no items have been graded yet.

        Rules:
            - Only items with points_earned != None count as graded.
            - Categories with no graded items are excluded from the calculation.
            - Use score_to_letter() to convert the final percentage to a letter grade.
            - Must not print anything.
        """
        # TODO: Implement the weighted grade algorithm described above
        pass


class CourseManager:
    def __init__(self):
        """
        Initialize the CourseManager with an empty list of courses.

        Instance variables to set:
            self.courses -- empty list (will hold Course objects)
        """
        # TODO: Set self.courses to an empty list
        pass

    def add_course(self, course):
        """
        Add a Course object to the manager's list.

        Parameters:
            course (Course): The Course object to add.

        Rules:
            - Must not print anything.
        """
        # TODO: Append course to self.courses
        pass

    def find_course(self, course_name):
        """
        Find and return a Course by name (case-insensitive).

        Parameters:
            course_name (str): The course name to search for.

        Returns:
            Course: The matching Course object, or None if not found.

        Rules:
            - Comparison must be case-insensitive.
            - Must not print anything.
        """
        # TODO: Loop through self.courses and return the matching course or None
        pass

    def find_course_by_code(self, course_code):
        """
        Find and return a Course by course code (case-insensitive).

        Parameters:
            course_code (str): The course code to search for (e.g., "ECE122").

        Returns:
            Course: The matching Course object, or None if not found.

        Rules:
            - Comparison must be case-insensitive.
            - Must not print anything.
        """
        # TODO: Loop through self.courses and match on course_code (case-insensitive)
        pass

    def display_courses(self):
        """
        Return a list of formatted strings for all courses.

        Format for each entry:
            "<course_code>: <course_name> (<instructor_name>)"

        Returns:
            list[str]: One string per course,
                       or ["No courses available."] if no courses have been added.
        """
        # TODO: Implement this method
        pass
