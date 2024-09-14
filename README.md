[![supermorph_PixelSnake_logo_v001](https://github.com/user-attachments/assets/0e92f76c-67db-4ff6-8e58-9ab77a9a6e8e)](https://www.supermorph.tech/)
<br><br><br>
![supermorph_morPy_github_v001](https://github.com/user-attachments/assets/51fd6975-d4cd-4123-b708-552e8fee9c1a)


More solutions. More insights. morPy.

Multiprocessing aided Python framework with integrated logging to database. Be the master of your app by analyzing runtime. Enjoy the comfort of runtime documentation ready for use in validated environments.

Feel free to comment, share and support this project.
Visit me on [supermorph.tech](https://www.supermorph.tech/) to get in touch with me.

# Versioning - α.β.γλ

| Symbol | Description |
| --- | --- |
| α   | Major Version.  <br>No downward compatibility: CRITICAL errors expected. |
| β   | Improvement Version.  <br>Limited downward compatibility: WARNING and DENIED messages expected. |
| γ   | Bugfix Version.  <br>Full downward compatibility. |
| λ   | Version status.  <br>*None*: Release version  <br>*a*: Alpha version with minor bugs for public testing.  <br>*b*: Beta version with potential showstopper bugs for internal testing.  <br>*c*: Gamma version. Development. Not presentable to public. |

# Parallelization

The parallelization in morPy is done utilizing an orchestration process with which the entire program starts and ends. The process ID "0" is always reserved for the orchestration process. It will take care of logging and is reserved for tasks with a priority in between 0 and 10 (smaller numbers for higher priority). All project tasks will automatically receive a higher number (lower priority) than morPy reserved tasks. In case a priority is corrected, a warning will be raised.

![EN-morPy-parallelization-scheme-v1 0 0-darkmode](https://github.com/user-attachments/assets/4f460193-7a01-4c78-a501-16b99aea747b)
