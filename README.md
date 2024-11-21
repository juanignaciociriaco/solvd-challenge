# 🚀 Solvd Challenge

This challenge involves creating a **main stack** and a **substack** with a single resource. The goal is to test the output of a Python script when the substack enters a rollback state.

## 📂 Repository Contents

The repository includes several scripts as explained below

## Notes

The Output.json iterates over the main stack. I would need more time —and therefore won't be submitting it on time— to write the code that picks up the name of the resource belonging to the substack that is failing.

### 🐧 🍏 Bash Scripts

1. **`0-UploadSubstackTemplatetoS3.sh`**  
   - Uploads the `Substack.yaml` file to AWS S3. If the S3 bucket doesn't exist, it creates it.
   - Usage:  
     ```bash
     ./0-UploadSubstackTemplatetoS3.sh
     ```

2. **`1-CreateStack.sh`**  
   - Manages the creation and update of the main stack.  
   - Usage modes:
     - **Create a stack**:  
       ```bash
       ./1-Stack.sh create
       ```
     - **Update a stack with an intentional error**:  
       Introduces an error in the S3 bucket name (a parameter in the `.yaml` file).  
       ```bash
       ./1-Stack.sh update
       ```
     - **Delete a stack with an intentional error**:  
      Deletes the main stack and its substack  
       ```bash
       ./1-Stack.sh delete
       ```       

3. **`2-Run-Python.sh`**  
   - Installs the necessary dependencies and runs the Python script.  
   - Usage:  
     ```bash
     ./2-Run-Python.sh
     ```

4. **`Output.json`**  
   - Displays the expected output from the Python script.  
   - To view it:  
     ```bash
     cat Output.json
     ```

---

## 📝 Notes

- This process simulates a **rollback** state in the substack to verify the Python script's response.  
- Ensure that AWS CLI is configured, and you have appropriate permissions before running the scripts.
