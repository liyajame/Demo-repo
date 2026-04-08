namespace Themovieratingapp;
sealed class Watchlist
{
    public string Name { get; set; }
    public List<Movie> Movies { get; private set; } = new List<Movie>();
    public Watchlist(string name, List<Movie> movies)
    {
        Name = name;
        Movies = new List<Movie>();
    }
    public override string ToString()
    {
        if (Movies == null || Movies.Count == 0)
        {
            return $"Watchlist: {Name}\nNo movies added yet. ";
        }
        else
        {
            var MoviesInfo = string.Join(Environment.NewLine, Movies.Select(m => m.ToString()));
            return $"Watchlist:{Name}\n{MoviesInfo}";

        }
    }
}


