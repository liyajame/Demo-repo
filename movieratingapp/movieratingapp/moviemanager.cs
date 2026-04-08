namespace Themovieratingapp;
sealed class MovieManager
{
    public List<Movie> Movies { get; private set; } 
    public MovieManager()
    {
        Movies = DataStorage.LoadMovies();
    }
    public void PrintMainMenu()
    {
        Console.WriteLine("\n\t|------------------Managaing Movie DataBase------------------|");
        Console.WriteLine("1. Add Movie\n2. Rate Movie\n3. View All Movies And Ratings\n4. Delete Movie \n5. Retrun To Main Menu");
    }
    public void HandleUserInput()
    {
        bool managingMovies = true;
        while (managingMovies)
        {
            PrintMainMenu();
            Console.Write("select an option: ");
            string option = Console.ReadLine();
            switch (option)
            {
                case "1":
                    AddMovie();
                    break;
                case "2":
                    RateMovie();
                    break;
                case "3":
                    ViewAllMoviesAndRatings();
                    break;
                case "4":
                    DeleteMovie();
                    break;
                case "5":
                    managingMovies = false;
                    break;
                default:
                    Console.WriteLine("Invalid option, please try again.");
                    break;
            }
        }
    }
    public void AddMovie()
    {
        Console.WriteLine("\n\t ===== ADDING MOVIE TO MOVIE DATABASE ===== ");
        Console.Write(" Enter movie name: ");
        string name = Console.ReadLine();
        while(Movies.Any(m => m.Name.Equals(name, StringComparison.OrdinalIgnoreCase)))
        {
            Console.WriteLine("This movie already exist. enter other name");
            return;
        }
        int year;
        while (true)
        {
            Console.Write("Enter year of release: ");
            if (int.TryParse(Console.ReadLine(), out year)&& year>0 && year<=2024)
            {
                break;
            }
            Console.WriteLine("Invalid Input, please valid year");
        }
        Console.Write("Enter director name: ");
        string director = Console.ReadLine();
        string type;
        while (true)
        {
            Console.Write("Enter type (1.Movie / 2. series: )");
            var typeInput = Console.ReadLine().Trim();
            if(typeInput == "1")
            {
                type = "Movie";
                    break;
            }
            else if(typeInput == "2")
            {
                type = "Series";
                break;
            }
            else
            {
                Console.WriteLine("Invalid Input, enter 1 for movie or 2 for series");
            }
        }
        Console.Write("Enter genre: ");
        string genre = Console.ReadLine();

        var movie = new Movie(name, year, director, type, genre);
        // TODO: Redundant check
        if (!Movies.Any(m => m.Name.Equals(name, StringComparison.OrdinalIgnoreCase)))
        {
            Movies.Add(movie);
            Console.WriteLine($"'{name}' added sucessfully. ");
        }
        else
        {
            Console.WriteLine("This movie already exists.");
        }
        DataStorage.SaveMovies(Movies);
    }
    private void RateMovie()
    {
        if (Movies.Count == 0)
        {
            Console.WriteLine("No Movies added Yet.");
            return;
        }
        Console.WriteLine("\n\t ===== ITS TIME TO RATE MOVIE!! ===== ");
        foreach (var r in Movies)
        {
            Console.WriteLine($"{Movies.IndexOf(r) + 1}. {r.Name}");

        }
        while (true)
        {
            Console.Write("Enter the id of the movie you wish to rate or enter q to quit: ");
            var id = Console.ReadLine();
            if (int.TryParse(id, out var index))
            {
                index--;
                if (index >= 0 && index < Movies.Count)
                {
                    while (true)
                    {
                        Console.Write($"Enter rating for {Movies[index].Name} (0.0 to 5.0): ");
                        // TODO: Double comparison
                        if (double.TryParse(Console.ReadLine(), out double rating) && rating >= 0 && rating <= 5)
                        {
                            Movies[index].Rating = rating;
                            Console.WriteLine($"Movie {Movies[index].Name} rated {rating} out of 5.0");
                            DataStorage.SaveMovies(Movies);
                            break;
                        }
                        else
                        {
                            Console.WriteLine("Invalid Rating. Please enter valid input: ");

                        }
                    }
                    break;
                    
                }
            }
            else if(id.ToLower() == "q")
            {
                break;
            }
            else
            {
                Console.Write("Invalid id.");

            }
            
        }
        
    }
    private void ViewAllMoviesAndRatings()
    {
        if (Movies.Any())
        {
            foreach (var movie in Movies)
            {
                Console.WriteLine(movie.ToString());
            }
        }
        else
        {
            Console.WriteLine("No movies added yet");
        }
    }
    private void DeleteMovie()
    {
        Console.WriteLine("\n\t ===== DELETE MOVIE FROM MOVIE DATABASE ===== ");
        if (Movies.Count == 0)
        {
            Console.WriteLine("No Movies added Yet.");
        }
        else
        {
            foreach (var m in Movies)
            {
                Console.WriteLine($"{Movies.IndexOf(m)}. {m.Name}");

            }
            
            while (true)
            {
                Console.Write("Enter the id of the movie you wish to delete or enter q to quit: ");
                var id = Console.ReadLine();
                if(id.ToLower() == "q")
                {
                    break;
                }
                if (int.TryParse(id, out var index) && index >= 0 && index < Movies.Count)
                {
                    var moviename = Movies[index];
                    Movies.RemoveAt(index);
                    Console.WriteLine($"Movie '{moviename.Name}' was deleted from list");
                    DataStorage.SaveMovies(Movies);
                    break;
                }
                else
                {
                    Console.Write("Your entry is Invalid. ");
                    
                }
            }
        }
    }
}
