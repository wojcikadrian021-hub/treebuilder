class EmployeeNode:
    """Represents one employee and their two possible direct reports."""

    def __init__(self, name):
        self.name = name
        self.left = None
        self.right = None


class TeamTree:
    """Stores the company reporting structure as a binary tree."""

    def __init__(self):
        self.root = None

    def insert(self, manager_name, employee_name, side, current_node=None):
        # Only the original call should print the unknown-manager error.
        top_call = current_node is None
        if current_node is None:
            current_node = self.root
            if current_node is None:
                print("❌ Add a team lead before adding employees.")
                return False

        side = side.lower().strip()
        if side not in ("left", "right"):
            print("❌ Side must be 'left' or 'right'.")
            return False

        if current_node.name == manager_name:
            if getattr(current_node, side) is not None:
                print(f"❌ The {side.upper()} side of {manager_name} is already taken.")
                return False

            new_employee = EmployeeNode(employee_name)
            if side == "left":
                current_node.left = new_employee
            else:
                current_node.right = new_employee
            print(f"✅ {employee_name} added to the {side.upper()} of {manager_name}")
            return True

        # Search the left branch, then the right branch.
        # Only recurse into real nodes so None never resets us to the root.
        if current_node.left is not None:
            if self.insert(manager_name, employee_name, side, current_node.left):
                return True
        if current_node.right is not None:
            if self.insert(manager_name, employee_name, side, current_node.right):
                return True

        if top_call:
            print(f"❌ Manager '{manager_name}' does not exist.")
        return False

    def print_tree(self, node=None, level=0):
        if node is None:
            if level == 0:
                node = self.root
            if node is None:
                if level == 0:
                    print("No team members yet.")
                return

        print("  " * level + "- " + node.name)
        self.print_tree(node.left, level + 1)
        self.print_tree(node.right, level + 1)

    def has_manager(self, manager_name, node=None):
        """Recursively check whether a manager exists, for helpful CLI errors."""
        if node is None:
            node = self.root
        if node is None:
            return False
        return self._contains(node, manager_name)

    def _contains(self, node, name):
        if node is None:
            return False
        return (node.name == name or
                self._contains(node.left, name) or
                self._contains(node.right, name))


def company_directory():
    tree = TeamTree()

    while True:
        print("\n📋 Team Management Menu")
        print("1. Add Team Lead (root)")
        print("2. Add Employee")
        print("3. Print Team Structure")
        print("4. Exit")

        choice = input("Choose an option (1–4): ")

        if choice == "1":
            if tree.root is not None:
                print("⚠️ Team lead already exists.")
            else:
                name = input("Enter team lead's name: ").strip()
                if not name:
                    print("❌ Name cannot be empty.")
                else:
                    tree.root = EmployeeNode(name)
                    print(f"✅ {name} added as the team lead.")

        elif choice == "2":
            manager = input("Enter the manager's name: ").strip()
            employee = input("Enter the new employee's name: ").strip()
            side = input("Should this employee be on the LEFT or RIGHT of the manager? ")
            if not manager or not employee:
                print("❌ Names cannot be empty.")
            elif tree.root is None:
                print("❌ Add a team lead before adding employees.")
            elif side.lower().strip() not in ("left", "right"):
                print("❌ Side must be 'left' or 'right'.")
            elif not tree.has_manager(manager):
                print(f"❌ Manager '{manager}' does not exist.")
            else:
                tree.insert(manager, employee, side)

        elif choice == "3":
            print("\n🌳 Current Team Structure:")
            tree.print_tree()

        elif choice == "4":
            print("Good Bye!")
            break

        else:
            print("❌ Invalid option. Try again.")


if __name__ == "__main__":
    company_directory()
