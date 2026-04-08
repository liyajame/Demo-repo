namespace Themovieratingapp;
sealed class WatchlistManager
{
    public List<Watchlist> Watchlists { get; private set; }
    private DataStorage _datastorage;

    public WatchlistManager()
    {
        Watchlists = DataStorage.LoadWatchlists();
    }
    public void printmenu()
    {
        Console.WriteLine("\n\t|------------------Managaing Watchlist DataBase------------------|");
        Console.WriteLine("\n1. Create Watchlist\n2. Add Movie To Watchlist\n3. View Watchlist\n4. Delete Watchlist\n5. Delete Movie From watchlist\n6. Return To Main Menu");
    }
    public void HandleUserInput()
    {
        bool mm = true;
        while (mm)
        {
            printmenu();
            Console.Write("Choose an option: ");
            string option = Console.ReadLine();
            switch (option)
            {
                case "1":
                    CreateWatchlist();
                    break;
                case "2":
                    AddMovieToWatchlist();
                    break;
                case "3":
                    ViewWatchlist();
                    break;
                case "4":
                    DeleteWatchlist();
                    break;
                case "5":
                    RemoveMovieFromWathlist(Watchlists, _datastorage);
                    break;
                case "6":
                    mm = false;
                    break;
                default:
                    Console.WriteLine("Invalid option, please try again.");
                    break;
            }
        }
    }
    private void CreateWatchlist()
    {
        Console.WriteLine("\n\t ===== LETS CREATE WATCHLIST! ===== ");
        Console.Write("Enter watchlist name: ");
        string name = Console.ReadLine();
        if (Watchlists.Any(w => w.Name.Equals(name, StringComparison.OrdinalIgnoreCase)))
        {
            Console.WriteLine("A watchlist with this name already exists.");
            return;
        }
        Watchlist newWatchlist = new Watchlist(name, new List<Movie>());
        Watchlists.Add(newWatchlist);
        DataStorage.SaveWatchlists(Watchlists);
        Console.WriteLine($"Watchlist '{name}' created successfully.");
    }
    private void ViewWatchlist()
    {
        Console.WriteLine("\n\t ===== EXISTING WATCHLISTS ===== ");
        if (Watchlists.Any())
        {
            foreach (var watchlist in Watchlists)
            {
                Console.WriteLine(watchlist.ToString());
            }
        }
        else
        {
            Console.WriteLine("No watchlists have been created yet.");
        }
    }
    private void AddMovieToWatchlist()
    {
        Console.WriteLine("\n\t ===== ADDING MOVIE TO WATCHLIST ===== ");
        if (Watchlists.Count == 0)
        {
            Console.WriteLine("No Watchlist Created Yet.");
            return;
        }
        List<Movie> allMovies = DataStorage.LoadMovies();
        foreach (var t in Watchlists)
        {
            Console.WriteLine($"{Watchlists.IndexOf(t)}. {t.Name}");
        }
        while (true)
        {
            Console.Write("Enter the id from which to add a movie: ");
            var index = Console.ReadLine();
            if (int.TryParse(index, out int watchlistIndex) && watchlistIndex >= 0 && watchlistIndex < Watchlists.Count)
            {
                while (true)
                {
                    Console.WriteLine("select id: 1. Add existing more or 2.add a new movie");
                    string option = Console.ReadLine();
                    if (option == "1")
                    {
                        Watchlist selectedwatchlist = Watchlists[watchlistIndex];
                        foreach (var movie in allMovies)
                        {
                            Console.WriteLine($"{allMovies.IndexOf(movie)} : {movie.Name}");
                        }
                        if (allMovies.Count == 0)
                        {
                            Console.WriteLine("No movies added yet");
                            break;
                        }
                        else
                        {
                            Console.Write("Above displayed are the available movies.  ");
                            Console.Write("Enter the movie number you wish to add.");
                            int movieIndex;
                            while (!int.TryParse(Console.ReadLine(), out movieIndex) && movieIndex < 0 || movieIndex > allMovies.Count)
                            {
                                Console.WriteLine("Invalid Input. enter a valid number: ");
                            }
                            Movie selectedMovie = allMovies[movieIndex];
                            if (!selectedwatchlist.Movies.Any(m => m.Name.Equals(selectedwatchlist.Name, StringComparison.OrdinalIgnoreCase)))
                            {
                                selectedwatchlist.Movies.Add(selectedMovie);
                                Console.WriteLine("Movie added SUCESSFULLY");
                            }

                            else
                            {
                                Console.WriteLine("Movie already exist");
                            }
                            DataStorage.SaveWatchlists(Watchlists);
                            //break;
                        }
                        break;
                        
                    }
                    else if (option == "2")
                    {
                        Console.WriteLine("Enter the name of the movie: ");
                        string movieName = Console.ReadLine();
                        Movie newMovie = new Movie(movieName, 0, null, null, null);
                        Watchlists[watchlistIndex].Movies.Add(newMovie);
                        Console.WriteLine($"newMovie {newMovie.Name} added.");
                        DataStorage.SaveMovies(allMovies);
                        Console.WriteLine($"{newMovie.Name} added.to watchlist ");
                        break;
                    }
                    else
                    {
                        Console.Write("Invalid input.  ");

                    }
                }
                break;

            }
            else
            {
                Console.Write("Invalid input. ");
            }

        }
    
    }
    private void DeleteWatchlist()
    {
        Console.WriteLine("\n\t ===== REMOVING MOVIE TO MOVIE DATABASE ===== ");
        if (Watchlists.Count == 0)
        {
            Console.WriteLine("No Watchlist Created Yet.");
        }
        else
        {
            foreach (var m in Watchlists)
            {
                Console.WriteLine($"{Watchlists.IndexOf(m)}. {m.Name}");
            }
            while (true)
            {
                Console.Write("Enter the id of the movie you wish to delete: ");
                if (int.TryParse(Console.ReadLine(), out int watchlistIndex) && watchlistIndex >= 0 && watchlistIndex < Watchlists.Count)
                {
                    var watchlistItem = Watchlists[watchlistIndex];
                    Watchlists.RemoveAt(watchlistIndex);
                    Console.WriteLine($" Watchlist '{watchlistItem.Name}' deleted");
                    DataStorage.SaveWatchlists(Watchlists);
                    break;
                }
                else
                {
                    Console.WriteLine("Invalid Input. ");
                }
            }
        }

    }
    private void RemoveMovieFromWathlist(List<Watchlist> watchlists, DataStorage dataStorage)
    {
        Console.WriteLine("\n\t ===== REMOVING MOVIE TO MOVIE DATABASE ===== ");
        if (Watchlists.Count == 0)
        {
            Console.WriteLine("No Watchlist Created Yet.");
        }
        else
        {
            foreach (var m in Watchlists)
            {
                Console.WriteLine($"{Watchlists.IndexOf(m)}. {m.Name}");
            }
            while (true)
            {

                Console.Write("Enter the id from which to remove a movie: ");
                if (int.TryParse(Console.ReadLine(), out int watchlistIndex) && watchlistIndex >= 0 && watchlistIndex < Watchlists.Count)
                {
                    Watchlist selectedWatchlist = Watchlists[watchlistIndex];
                    Console.WriteLine($"Selected Watchlist: {selectedWatchlist.Name}");
                    foreach (var movie in selectedWatchlist.Movies)
                    {
                        Console.WriteLine($"{selectedWatchlist.Movies.IndexOf(movie)}. {movie.Name}");
                    }
                        if (selectedWatchlist.Movies.Count == 0)
                        {
                            Console.WriteLine("No movies added to Watchlist yet.");
                            break;
                        }
                        else
                        {

                        while (true)
                        {
                            Console.Write("Enter the id of the movie you want to delete.: ");

                            if (int.TryParse(Console.ReadLine(), out int movieIndex) && movieIndex >= 0 && movieIndex < selectedWatchlist.Movies.Count)
                            {
                                Movie movieToRemove = selectedWatchlist.Movies[movieIndex];
                                selectedWatchlist.Movies.RemoveAt(movieIndex);
                                Console.WriteLine($"Movie {movieToRemove.Name} was deleted from {selectedWatchlist.Name}");
                                DataStorage.SaveWatchlists(Watchlists);
                                break;
                            }
                            else
                            {
                                Console.WriteLine("Invalid Input. ");
                            }
                        }

                        }
                    break;
                    }
                else
                {
                    Console.WriteLine("Invalid input");
                }
            }
        }
    }
}