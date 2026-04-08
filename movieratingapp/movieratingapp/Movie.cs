namespace Themovieratingapp;
sealed class Movie
{
    public string Name { get; set; }
    public int Year { get; set; }
    public string Director { get; set; }
    public string Type { get; set; }
    public string Genre { get; set; }
    public double Rating { get; set; }
    public Movie(string name, int year, string director, string type,  string genre)
    {
        Name = name;
        Year = year;
        Director = director;
        Type = type;
        Genre = genre;
    }
    public override string ToString()
    {
        return $"{Name} ({Year}), Directed by {Director}, Type: {Type}, Genre: {Genre}, Average Rating: {Rating:0.0}/5.0";
    }
}



