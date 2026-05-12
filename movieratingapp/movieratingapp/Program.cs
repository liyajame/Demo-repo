using System.IO;
using System.Linq;
using System.Text.Json;
using System.Collections.Generic;
using System.Net.Http.Headers;

namespace Themovieratingapp;
static class Program
{
    private static List<Movie> Movies;
    private static List<Watchlist> Watchlists;
    static void Main(string[] args)
    { 
        MovieManager movieManager = new MovieManager();
        WatchlistManager watchlistManager = new WatchlistManager();
        Console.WriteLine("\n\t\t\t\tWELCOME TO MOVIE RATING APP!!!");
        bool running = true;
        while (running)
        {
            Console.WriteLine("\n\t========Menu Manager==========");
            Console.WriteLine("1. Manage Movie Database\n2. Manage watchlist database. \n3. Exit ");
            Console.Write("Select an option:  ");
            var option = Console.ReadLine();

            switch (option)
            {
                case "1":
                    movieManager.HandleUserInput();
                    break;
                case "2":
                    watchlistManager.HandleUserInput();
                    break;
                case "3":
                    DataStorage.SaveData(Movies, Watchlists); 
                    running = false;
                    Console.WriteLine("-------Exiting the program----------");
                    break;
                default:
                    Console.WriteLine("Invalid option, please try again.");
                    break;
            }
        }
        DataStorage.SaveData(movieManager.Movies, watchlistManager.Watchlists); 
    }
}
       
