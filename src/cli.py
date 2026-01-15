import cmd
import shlex
import sys
from src.db.core import Database

class DatabaseShell(cmd.Cmd):
    intro = 'Welcome to the Pesapal RDBMS REPL. Type help or ? to list commands.\nType "exit" or "quit" to leave.'
    prompt = '(db) '
    
    def __init__(self, db_path="db.json"):
        super().__init__()
        self.db = Database(db_path)
        self.db.load()
        print(f"Database loaded from {db_path}")

    def default(self, line):
        """Handle execution of SQL keys."""
        if line.lower() in ('exit', 'quit'):
            return True
        
        # Simple fix for empty lines causing issues
        if not line.strip():
            return

        try:
            # Debugging: print what we received
            # print(f"DEBUG: Processing '{line}'") 
            result = self.db.execute_query(line)
            self._print_result(result)
        except Exception as e:
            print(f"Error: {e}")

    def do_EOF(self, arg):
        """Handle EOF (Ctrl+D) to exit gracefully."""
        print() # Newline
        return True

    def _print_result(self, result):
        if isinstance(result, list):
            if not result:
                print("Empty set")
            else:
                # Pretty print list of dicts
                headers = list(result[0].keys())
                print(" | ".join(headers))
                print("-" * (len(headers) * 10))
                for row in result:
                    print(" | ".join(str(row.get(h, 'NULL')) for h in headers))
                print(f"\n({len(result)} rows)")
        else:
            print(result)

    def do_exit(self, arg):
        """Exit the REPL"""
        print("Saving database...")
        self.db.save()
        print("Goodbye.")
        return True

    def do_quit(self, arg):
        """Exit the REPL"""
        return self.do_exit(arg)

    def do_save(self, arg):
        """Manually save the database to disk."""
        self.db.save()
        print("Database saved.")

if __name__ == '__main__':
    try:
        DatabaseShell().cmdloop()
    except KeyboardInterrupt:
        print("\nExiting...")
