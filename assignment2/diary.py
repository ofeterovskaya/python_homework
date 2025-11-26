# Task 1: Diary
import traceback

def main():
    try:
        first_prompt = True

        # Open diary.txt for appending; `with` guarantees the file closes even on exceptions
        with open("diary.txt", "a", encoding="utf-8") as f:
            while True:
                prompt = "What happened today? " if first_prompt else "What else? "
                first_prompt = False

                line = input(prompt).strip() # Get a line from the user

                f.write(line + "\n") # Write the line immediately, always with a newline

                if line == "done for now": # Stop when the special line is received 
                    break

    except Exception as e:
        trace_back = traceback.extract_tb(e.__traceback__)
        stack_trace = []
        for trace in trace_back:
            stack_trace.append(
                f"File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}"
            )

        print("An exception occurred.")
        print(f"Exception type: {type(e).__name__}")
        message = str(e)
        if message:
            print(f"Exception message: {message}")
        print(f"Stack trace: {stack_trace}")


if __name__ == "__main__":
    main()

