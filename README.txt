Welcome to my first personal project, as part of the Boot.dev curriculum. 

About:
The thought of doing my first unguided project has filled me with trepidation since doing my first guided project, and as such, regardless of how barebones and simple this little Tkinter GUI application may be (I admit, the UI is barbaric at best), I consider this a huge milestone for me. 

I learned about creating functionality side by side with Tkinter, developed a better understanding of how Tkinter works, saving and loading using JSON, and generally have gotten a better understanding of how I should structure my code and workflow the next time I start a project. I also took the chance to pick up Neovim before I started this. Needless to say -- some limits were pushed.

I originally intended to build a library that collected info about the books stored in them, and would output statistics about your reading habits, such as how much you spent on books over time, an overview of the genres you were into (bar charts would have been involved). But due to a mixture of confusion about my priorities and incompetence as someone who has a whopping track record of 4 months of coding, I settled on a simple library GUI app that kept track of the books you were reading, wanting to read, or have finished. It took me a whole month to make as I had to constantly learn about new concepts and topics that I wouldn't otherwise have gotten around to. Though to be honest, at this point, I just want to be done with it and move on to the next part of the course.

How to install:
1. Go to the "Dist" folder and download the Linux/Windows executable, depending on your OS. (.exe is for Windows)
2. If you're on Linux, type "chmod +x path/to/your/executable". For example: if librarie is in "~/Downloads/", move to that directory in your terminal and run "chmod +x librarie" . In Windows, Windows Defender will show up. Simply click "more info" and then "Run anyway"
3. Run it.
4. Load from a save file or close the dialog box to start a fresh library. 
5. When you exit, the library will prompt you to save a JSON file, from which you can load your library next time.

How to use:
Home page: After loading a file (or not), you may create, delete, or load your libraries. Think of them as save files in a video games. You may assign different sets of books to each library, but you would probably stick to 1 most of the time.
Dashboard: Here you have a snapshot of the books in your library, segregated into 3 categories (Reading, Unread, Finished). Clicking on each of them will show you their info on the right side of the dashboard. You can also input some notes on the bottom right box for the book you have selected.
Menubar - Books Tab: Create or Edit your books. Books created are shared across all libraries.
Menubar - Manage Tab: Manage your books and libraries. All the books created are shown here, and you may assign each book to the libraries you prefer, remove books from their libraries, add new libraries, or delete libraries. You can also choose to switch libraries or rename your current library.
Save - Simply close the program, a prompt will ask you to save.

Note:
I used PyInstaller to make the executable for both Linux and Windows. For some reason, the windows executable **may** takes ages to load, but it does load. Both programs may say that its dangerous to run them due to the creator being unidentified (That is expected).

Features in the future, perhaps:
- Open Library API Integration
- PDF Storage
- More colours ? (probably not)

