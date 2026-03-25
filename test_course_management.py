import unittest
from course_management import CourseItem, Course, CourseManager, DEFAULT_WEIGHTS, score_to_letter


# =============================================================================
# Test 1 — CourseItem: Creation & Basic Methods
# =============================================================================

class TestCourseItemCreation(unittest.TestCase):
    """Test that CourseItem initializes all attributes correctly."""

    def test_attributes_set_correctly(self):
        item = CourseItem("HW1", "Homework", "2026-03-20", 100)
        self.assertEqual(item.title, "HW1")
        self.assertEqual(item.category, "Homework")
        self.assertEqual(item.due_date, "2026-03-20")
        self.assertEqual(item.points_possible, 100)

    def test_points_earned_starts_as_none(self):
        item = CourseItem("Quiz 1", "Quiz", "2026-03-21", 20)
        self.assertIsNone(item.points_earned)

    def test_completed_starts_as_false(self):
        item = CourseItem("Exam 1", "Exam", "2026-03-25", 100)
        self.assertFalse(item.completed)


class TestCourseItemMethods(unittest.TestCase):
    """Test mark_complete, update_score, and display_info."""

    def test_mark_complete_sets_flag(self):
        item = CourseItem("HW2", "Homework", "2026-03-22", 50)
        item.mark_complete()
        self.assertTrue(item.completed)

    def test_mark_complete_idempotent(self):
        item = CourseItem("HW2", "Homework", "2026-03-22", 50)
        item.mark_complete()
        item.mark_complete()
        self.assertTrue(item.completed)

    def test_update_score_sets_points_earned(self):
        item = CourseItem("Exam 1", "Exam", "2026-03-25", 100)
        item.update_score(92)
        self.assertEqual(item.points_earned, 92)

    def test_update_score_can_be_overwritten(self):
        item = CourseItem("Exam 1", "Exam", "2026-03-25", 100)
        item.update_score(80)
        item.update_score(95)
        self.assertEqual(item.points_earned, 95)

    def test_display_info_not_graded_incomplete(self):
        item = CourseItem("HW1", "Homework", "2026-03-20", 100)
        result = item.display_info()
        self.assertIn("HW1", result)
        self.assertIn("Homework", result)
        self.assertIn("2026-03-20", result)
        self.assertIn("Not graded", result)
        self.assertIn("Incomplete", result)

    def test_display_info_graded_completed(self):
        item = CourseItem("Quiz 1", "Quiz", "2026-03-21", 20)
        item.update_score(18)
        item.mark_complete()
        result = item.display_info()
        self.assertIn("18", result)
        self.assertIn("20", result)
        self.assertIn("Completed", result)
        self.assertNotIn("Not graded", result)

    def test_display_info_format(self):
        # Verify the exact pipe-separated format
        item = CourseItem("HW1", "Homework", "2026-03-20", 100)
        item.update_score(85)
        result = item.display_info()
        expected = "Homework: HW1 | Due: 2026-03-20 | Score: 85/100 | Status: Incomplete"
        self.assertEqual(result, expected)


# =============================================================================
# Test 2 — score_to_letter
# =============================================================================

class TestScoreToLetter(unittest.TestCase):
    """Test the full letter grade scale including all +/- grades."""

    def test_A(self):
        self.assertEqual(score_to_letter(100), "A")
        self.assertEqual(score_to_letter(93),  "A")

    def test_A_minus(self):
        self.assertEqual(score_to_letter(90), "A-")
        self.assertEqual(score_to_letter(92), "A-")

    def test_B_plus(self):
        self.assertEqual(score_to_letter(87), "B+")
        self.assertEqual(score_to_letter(89), "B+")

    def test_B(self):
        self.assertEqual(score_to_letter(83), "B")
        self.assertEqual(score_to_letter(86), "B")

    def test_B_minus(self):
        self.assertEqual(score_to_letter(80), "B-")
        self.assertEqual(score_to_letter(82), "B-")

    def test_C_plus(self):
        self.assertEqual(score_to_letter(77), "C+")
        self.assertEqual(score_to_letter(79), "C+")

    def test_C(self):
        self.assertEqual(score_to_letter(73), "C")
        self.assertEqual(score_to_letter(76), "C")

    def test_C_minus(self):
        self.assertEqual(score_to_letter(70), "C-")
        self.assertEqual(score_to_letter(72), "C-")

    def test_D_plus(self):
        self.assertEqual(score_to_letter(67), "D+")
        self.assertEqual(score_to_letter(69), "D+")

    def test_D(self):
        self.assertEqual(score_to_letter(63), "D")
        self.assertEqual(score_to_letter(66), "D")

    def test_D_minus(self):
        self.assertEqual(score_to_letter(60), "D-")
        self.assertEqual(score_to_letter(62), "D-")

    def test_F(self):
        self.assertEqual(score_to_letter(59),  "F")
        self.assertEqual(score_to_letter(0),   "F")


# =============================================================================
# Test 3 — Course: Item Management
# =============================================================================

class TestCourseItemManagement(unittest.TestCase):
    """Test add_item, find_item, remove_item, display_items, display_pending_items."""

    def setUp(self):
        self.course = Course("Intro to Python", "ECE122", "Prof. Smith")

    def test_starts_with_no_items(self):
        self.assertEqual(len(self.course.items), 0)

    def test_add_item(self):
        item = CourseItem("HW1", "Homework", "2026-03-20", 100)
        self.course.add_item(item)
        self.assertEqual(len(self.course.items), 1)
        self.assertEqual(self.course.items[0].title, "HW1")

    def test_add_multiple_items(self):
        for i in range(3):
            self.course.add_item(CourseItem(f"HW{i}", "Homework", "2026-03-20", 10))
        self.assertEqual(len(self.course.items), 3)

    def test_find_item_found(self):
        item = CourseItem("HW1", "Homework", "2026-03-20", 100)
        self.course.add_item(item)
        found = self.course.find_item("HW1")
        self.assertIsNotNone(found)
        self.assertEqual(found.title, "HW1")

    def test_find_item_case_insensitive(self):
        self.course.add_item(CourseItem("HW1", "Homework", "2026-03-20", 100))
        self.assertIsNotNone(self.course.find_item("hw1"))
        self.assertIsNotNone(self.course.find_item("HW1"))
        self.assertIsNotNone(self.course.find_item("Hw1"))

    def test_find_item_not_found_returns_none(self):
        self.assertIsNone(self.course.find_item("nonexistent"))

    def test_remove_item_success(self):
        self.course.add_item(CourseItem("HW1", "Homework", "2026-03-20", 100))
        result = self.course.remove_item("HW1")
        self.assertTrue(result)
        self.assertEqual(len(self.course.items), 0)

    def test_remove_item_case_insensitive(self):
        self.course.add_item(CourseItem("HW1", "Homework", "2026-03-20", 100))
        result = self.course.remove_item("hw1")
        self.assertTrue(result)
        self.assertEqual(len(self.course.items), 0)

    def test_remove_item_not_found_returns_false(self):
        result = self.course.remove_item("ghost")
        self.assertFalse(result)

    def test_display_items_empty(self):
        result = self.course.display_items()
        self.assertEqual(result, ["No items found."])

    def test_display_items_returns_list_of_strings(self):
        self.course.add_item(CourseItem("HW1", "Homework", "2026-03-20", 100))
        self.course.add_item(CourseItem("Quiz 1", "Quiz", "2026-03-22", 20))
        result = self.course.display_items()
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], str)

    def test_display_pending_items_all_incomplete(self):
        self.course.add_item(CourseItem("HW1", "Homework", "2026-03-20", 100))
        self.course.add_item(CourseItem("HW2", "Homework", "2026-03-21", 100))
        result = self.course.display_pending_items()
        self.assertEqual(len(result), 2)

    def test_display_pending_items_filters_completed(self):
        hw1 = CourseItem("HW1", "Homework", "2026-03-20", 100)
        hw2 = CourseItem("HW2", "Homework", "2026-03-21", 100)
        hw1.mark_complete()
        self.course.add_item(hw1)
        self.course.add_item(hw2)
        result = self.course.display_pending_items()
        self.assertEqual(len(result), 1)
        self.assertIn("HW2", result[0])

    def test_display_pending_items_all_complete(self):
        item = CourseItem("HW1", "Homework", "2026-03-20", 100)
        item.mark_complete()
        self.course.add_item(item)
        result = self.course.display_pending_items()
        self.assertEqual(result, ["No pending items."])


# =============================================================================
# Test 4 — Course: Weight Management
# =============================================================================

class TestCourseWeights(unittest.TestCase):
    """Test set_weights, display_weights, and DEFAULT_WEIGHTS initialization."""

    def setUp(self):
        self.course = Course("Intro to Python", "ECE122", "Prof. Smith")

    def test_default_weights_sum_to_100(self):
        self.assertAlmostEqual(sum(DEFAULT_WEIGHTS.values()), 100.0)

    def test_course_inherits_default_weights(self):
        self.assertEqual(self.course.weights, DEFAULT_WEIGHTS)

    def test_course_weights_are_independent_copy(self):
        # Changing one course's weights must not affect another course
        other = Course("Circuits", "ECE101", "Prof. Jones")
        self.course.set_weights({"Homework": 50, "Quiz": 50, "Exam": 0,
                                  "Lecture Note": 0, "Project": 0})
        self.assertEqual(other.weights, DEFAULT_WEIGHTS)

    def test_set_weights_valid(self):
        new_w = {"Homework": 30, "Quiz": 30, "Exam": 30,
                 "Lecture Note": 5, "Project": 5}
        result = self.course.set_weights(new_w)
        self.assertTrue(result)
        self.assertEqual(self.course.weights["Homework"], 30)

    def test_set_weights_invalid_does_not_update(self):
        original = dict(self.course.weights)
        bad_w = {"Homework": 10, "Quiz": 10, "Exam": 10,
                 "Lecture Note": 10, "Project": 10}  # sums to 50
        result = self.course.set_weights(bad_w)
        self.assertFalse(result)
        self.assertEqual(self.course.weights, original)

    def test_display_weights_returns_list(self):
        result = self.course.display_weights()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), len(self.course.weights))

    def test_display_weights_contains_category_and_percent(self):
        result = self.course.display_weights()
        combined = " ".join(result)
        self.assertIn("Homework", combined)
        self.assertIn("%", combined)


# =============================================================================
# Test 5 — Course: calculate_grade
# =============================================================================

class TestCalculateGrade(unittest.TestCase):
    """Test the weighted grade calculation and letter grade output."""

    def setUp(self):
        self.course = Course("Intro to Python", "ECE122", "Prof. Smith")

    def test_no_graded_items_returns_none(self):
        self.course.add_item(CourseItem("HW1", "Homework", "2026-03-20", 100))
        self.assertIsNone(self.course.calculate_grade())

    def test_empty_course_returns_none(self):
        self.assertIsNone(self.course.calculate_grade())

    def test_returns_tuple(self):
        hw = CourseItem("HW1", "Homework", "2026-03-20", 100)
        hw.update_score(90)
        self.course.add_item(hw)
        result = self.course.calculate_grade()
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

    def test_percentage_and_letter_in_tuple(self):
        hw = CourseItem("HW1", "Homework", "2026-03-20", 100)
        hw.update_score(93)
        self.course.add_item(hw)
        pct, letter = self.course.calculate_grade()
        self.assertIsInstance(pct, float)
        self.assertIsInstance(letter, str)

    def test_single_category_correct_percentage(self):
        # Only homework graded: 80/100 = 80% -> weight is 20% of 20% active = 80%
        hw = CourseItem("HW1", "Homework", "2026-03-20", 100)
        hw.update_score(80)
        self.course.add_item(hw)
        pct, letter = self.course.calculate_grade()
        self.assertAlmostEqual(pct, 80.0)
        self.assertEqual(letter, "B-")

    def test_multiple_categories_weighted_correctly(self):
        # Homework 20%: 90/100 = 90%
        # Quiz 20%:     40/50  = 80%
        # Exam 40%:     70/100 = 70%
        # Active weight = 80, weighted_sum = 90*20 + 80*20 + 70*40 = 1800+1600+2800 = 6200
        # overall = 6200 / 80 = 77.5 -> C+
        hw = CourseItem("HW1", "Homework", "2026-03-20", 100)
        hw.update_score(90)
        q = CourseItem("Quiz 1", "Quiz", "2026-03-22", 50)
        q.update_score(40)
        e = CourseItem("Exam 1", "Exam", "2026-03-25", 100)
        e.update_score(70)
        self.course.add_item(hw)
        self.course.add_item(q)
        self.course.add_item(e)
        pct, letter = self.course.calculate_grade()
        self.assertAlmostEqual(pct, 77.5)
        self.assertEqual(letter, "C+")

    def test_multiple_items_in_same_category(self):
        # Two homeworks: 80/100 + 90/100 = 170/200 = 85%
        hw1 = CourseItem("HW1", "Homework", "2026-03-20", 100)
        hw1.update_score(80)
        hw2 = CourseItem("HW2", "Homework", "2026-03-21", 100)
        hw2.update_score(90)
        self.course.add_item(hw1)
        self.course.add_item(hw2)
        pct, letter = self.course.calculate_grade()
        self.assertAlmostEqual(pct, 85.0)
        self.assertEqual(letter, "B")

    def test_ungraded_items_excluded(self):
        # Graded: HW 90/100. Ungraded quiz should not affect result.
        hw = CourseItem("HW1", "Homework", "2026-03-20", 100)
        hw.update_score(90)
        q = CourseItem("Quiz 1", "Quiz", "2026-03-22", 50)  # not graded
        self.course.add_item(hw)
        self.course.add_item(q)
        pct, _ = self.course.calculate_grade()
        self.assertAlmostEqual(pct, 90.0)

    def test_custom_weights_applied(self):
        # Set exam to 100%, everything else 0%
        self.course.set_weights({"Homework": 0, "Quiz": 0, "Exam": 100,
                                  "Lecture Note": 0, "Project": 0})
        hw = CourseItem("HW1", "Homework", "2026-03-20", 100)
        hw.update_score(100)  # should be ignored
        e = CourseItem("Exam 1", "Exam", "2026-03-25", 100)
        e.update_score(65)
        self.course.add_item(hw)
        self.course.add_item(e)
        pct, letter = self.course.calculate_grade()
        self.assertAlmostEqual(pct, 65.0)
        self.assertEqual(letter, "D")

    def test_perfect_score(self):
        hw = CourseItem("HW1", "Homework", "2026-03-20", 100)
        hw.update_score(100)
        self.course.add_item(hw)
        pct, letter = self.course.calculate_grade()
        self.assertAlmostEqual(pct, 100.0)
        self.assertEqual(letter, "A")

    def test_zero_score(self):
        hw = CourseItem("HW1", "Homework", "2026-03-20", 100)
        hw.update_score(0)
        self.course.add_item(hw)
        pct, letter = self.course.calculate_grade()
        self.assertAlmostEqual(pct, 0.0)
        self.assertEqual(letter, "F")


# =============================================================================
# Test 6 — CourseManager
# =============================================================================

class TestCourseManager(unittest.TestCase):
    """Test CourseManager: add_course, find_course, find_course_by_code, display_courses."""

    def setUp(self):
        self.manager = CourseManager()
        self.c1 = Course("Intro to Python", "ECE122", "Prof. Smith")
        self.c2 = Course("Circuits I", "ECE101", "Prof. Jones")

    def test_starts_empty(self):
        self.assertEqual(len(self.manager.courses), 0)

    def test_add_course(self):
        self.manager.add_course(self.c1)
        self.assertEqual(len(self.manager.courses), 1)

    def test_add_multiple_courses(self):
        self.manager.add_course(self.c1)
        self.manager.add_course(self.c2)
        self.assertEqual(len(self.manager.courses), 2)

    def test_find_course_found(self):
        self.manager.add_course(self.c1)
        found = self.manager.find_course("Intro to Python")
        self.assertIsNotNone(found)
        self.assertEqual(found.course_code, "ECE122")

    def test_find_course_case_insensitive(self):
        self.manager.add_course(self.c1)
        self.assertIsNotNone(self.manager.find_course("intro to python"))
        self.assertIsNotNone(self.manager.find_course("INTRO TO PYTHON"))

    def test_find_course_not_found(self):
        self.assertIsNone(self.manager.find_course("Nonexistent"))

    def test_find_course_by_code_found(self):
        self.manager.add_course(self.c1)
        found = self.manager.find_course_by_code("ECE122")
        self.assertIsNotNone(found)
        self.assertEqual(found.course_name, "Intro to Python")

    def test_find_course_by_code_case_insensitive(self):
        self.manager.add_course(self.c1)
        self.assertIsNotNone(self.manager.find_course_by_code("ece122"))
        self.assertIsNotNone(self.manager.find_course_by_code("Ece122"))

    def test_find_course_by_code_not_found(self):
        self.assertIsNone(self.manager.find_course_by_code("MATH999"))

    def test_display_courses_empty(self):
        result = self.manager.display_courses()
        self.assertEqual(result, ["No courses available."])

    def test_display_courses_format(self):
        self.manager.add_course(self.c1)
        result = self.manager.display_courses()
        self.assertEqual(len(result), 1)
        self.assertIn("ECE122", result[0])
        self.assertIn("Intro to Python", result[0])
        self.assertIn("Prof. Smith", result[0])

    def test_display_courses_multiple(self):
        self.manager.add_course(self.c1)
        self.manager.add_course(self.c2)
        result = self.manager.display_courses()
        self.assertEqual(len(result), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
