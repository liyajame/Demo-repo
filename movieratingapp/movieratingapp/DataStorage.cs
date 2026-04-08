using System.Text.Json;
namespace Themovieratingapp;
sealed class DataStorage
{ 
    private const string MoviesFileName = "Movies.json";
    private const string WatchlistsFileName = "Watchlists.json";

    public static void SaveData(List<Movie> movies, List<Watchlist> watchlists)
    {
        SaveMovies(movies);
        SaveWatchlists(watchlists);
    }
    public static void SaveMovies(List<Movie> movies)
    {
        try
        {
            string json = JsonSerializer.Serialize(movies, new JsonSerializerOptions { WriteIndented = true });
            File.WriteAllText(MoviesFileName, json);
            Console.WriteLine("Data Saved successfully. ");
        }
        catch(Exception ex)
        {
            Console.WriteLine($"An error occurred while saving data: {ex.Message}");
        }
    }
    public static void SaveWatchlists(List<Watchlist> watchlists)
    {
        try
        {
            var watchlistsToSave = watchlists.Select(w1 => new { w1.Name, Movies = w1.Movies.Select(m => m.Name).ToList() });
            string json = JsonSerializer.Serialize(watchlists, new JsonSerializerOptions { WriteIndented = true });

            File.WriteAllText(WatchlistsFileName, json);
            Console.WriteLine("Watchlists saved sucessfully. ");
        }
        catch(Exception ex)
        {
            Console.WriteLine($"An error occurred while saving data: {ex.Message}");
        }
    }
    public static List<Movie> LoadMovies()
    {
        try
        {
            if (File.Exists(MoviesFileName))
            {
                string moviesJson = File.ReadAllText(MoviesFileName);
                return JsonSerializer.Deserialize<List<Movie>>(moviesJson) ?? new List<Movie>();
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"An error occurred while loading movies: {ex.Message}");
        }
        return new List<Movie>();
    }

    public static List<Watchlist> LoadWatchlists()
    {
        var movies = LoadMovies();
        try
        {
            if (File.Exists(WatchlistsFileName))
            {
                string watchlistsJson = File.ReadAllText(WatchlistsFileName);
                return JsonSerializer.Deserialize<List<Watchlist>>(watchlistsJson) ?? new List<Watchlist>();
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"An error occurred while loading watchlists: {ex.Message}");
        }
        return new List<Watchlist>();
    }
    private class WatchlistData
    {
        public string Name { get; set; }
        public List<string> Movies { get; set; }
    }
}
