using System.IO;
using System.Linq;
using System.Text.Json;
using System.Collections.Generic;
using System.Net.Http.Headers;

namespace Themovieratingapp;

// Review Comments for Code:
//  1) Watchlist -> Add Movie should insert into the main movies storage and not maintain its own separate and independent lists
//  2) Disallow duplicate movies in watchlist
//  3) Handle dependency of Watchlists on Movies without accessing the disk every time you add a movie to a watchlist
//  4) Menus and prompts should be indicative of what they are going to do.
//  5) In cases where specific options are available (i.e Add Movie -> Select Type (Movie/Series)) consider prompting user to type a number such as 1 for Movie, 2 for Series - partially done
//  6) Remove any unused code, namespaces, etc
//  7) Follow code standards for spacing, static vs sealed vs etc
//  8) Make sure your menus and prompts feel consistent to the user
//  9) Ensuring punctuation and or spelling for sentences.

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
       