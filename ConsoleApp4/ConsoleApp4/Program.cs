using System;
using System.Collections.Generic;
using System.IO;

class Program
{
    static void Main(string[] args)
    {
        var watchlist = new Watchlist();
        bool running = true;

        while (running)
        {
            Console.WriteLine("1. Add Movie\n2. Remove Movie\n3. View Watchlist\n4. Create Watchlist\n5. Exit");
            Console.Write("Select an option: ");
            var option = Console.ReadLine();

            switch (option)
            {
                case "1":
                    AddMovieToWatchlist(watchlist);
                    break;
                case "2":
                    RemoveMovieFromWatchlist(watchlist);
                    break;
                case "3":
                    ViewWatchlist(watchlist);
                    break;
                case "4":
                    CreateWatchlist(watchlist);
                    break;
                case "5":
                    running = false;
                    break;
                default:
                    Console.WriteLine("Invalid option, please try again.");
                    break;
            }
        }
    }

    static void AddMovieToWatchlist(Watchlist watchlist)
    {
        Console.Write("Enter movie name: ");
        string name = Console.ReadLine();
        Console.Write("Enter year of release: ");
        int year = Convert.ToInt32(Console.ReadLine());
        Console.Write("Enter director name: ");
        string director = Console.ReadLine();
        Console.Write("Enter type (Movie/Series): ");
        string type = Console.ReadLine();
        Console.Write("Enter genre: ");
        string genre = Console.ReadLine();

        var movie = new Movie(name, year, director, type, genre);
        watchlist.AddMovie(movie);
        SaveWatchlistToFile(watchlist);
    }

    static void RemoveMovieFromWatchlist(Watchlist watchlist)
    {
        Console.Write("Enter movie name to remove: ");
        var nameToRemove = Console.ReadLine();
        watchlist.RemoveMovie(nameToRemove);
        SaveWatchlistToFile(watchlist);
    }

    static void ViewWatchlist(Watchlist watchlist)
    {
        foreach (var movie in watchlist.Movies)
        {
            Console.WriteLine($"{movie.Name} ({movie.YearOfRelease}), {movie.Director}, {movie.Type}, {movie.Genre}");
        }
    }

    static void CreateWatchlist(Watchlist watchlist)
    {
        Console.Write("Enter watchlist name: ");
        watchlist.Name = Console.ReadLine();
    }

    static void SaveWatchlistToFile(Watchlist watchlist)
    {
        var path = $"{watchlist.Name}.txt";
        using (var writer = new StreamWriter(path, false))
        {
            foreach (var movie in watchlist.Movies)
            {
                writer.WriteLine($"{movie.Name},{movie.YearOfRelease},{movie.Director},{movie.Type},{movie.Genre}");
            }
        }
        Console.WriteLine("Watchlist saved.");
    }
}

public class Movie
{
    public string Name { get; set; }
    public int YearOfRelease { get; set; }
    public string Director { get; set; }
    public string Type { get; set; } // Movie or Series
    public string Genre { get; set; }

    public Movie(string name, int yearOfRelease, string director, string type, string genre)
    {
        Name = name;
        YearOfRelease = yearOfRelease;
        Director = director;
        Type = type;
        Genre = genre;
    }
}

public class Watchlist
{
    public string Name { get; set; }
    public List<Movie> Movies { get; set; } = new List<Movie>();

    public void AddMovie(Movie movie)
    {
        Movies.Add(movie);
    }

    public void RemoveMovie(string movieName)
    {
        Movies.RemoveAll(movie => movie.Name.Equals(movieName, StringComparison.OrdinalIgnoreCase));
    }
}