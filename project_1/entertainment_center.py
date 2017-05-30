import media
import fresh_tomatoes

shawshank = media.Movie(
            "The Shawshank Redemption",
            "Two imprisoned men bond over a number of years, finding\
            solace and eventual redemption through acts of common decency",
            "https://images-na.ssl-images-amazon.com/images/M/MV5BODU4MjU4NjIwNl5BMl5BanBnXkFtZTgwMDU2MjEyMDE@._V1_QL50_SY1000_CR0,0,672,1000_AL_.jpg",    # noqa
            "https://www.youtube.com/watch?v=6hB3S9bIaco")

inception = media.Movie(
            "Inception",
            "A thief, who steals corporate secrets through use of dream-sharing\
            technology, is given the inverse task of planting an idea into the\
            mind of a CEO",
            "https://images-na.ssl-images-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_QL50_SY1000_CR0,0,675,1000_AL_.jpg",    # noqa
            "https://www.youtube.com/watch?v=JEv8W3pWqH0")

saving_ryan = media.Movie(
            "Saving Private Ryan",
            "Following the Normandy Landings,\
            a group of U.S. soldiers go behind enemy lines to retrieve a\
            paratrooper whose brothers have been killed in action",
            "https://images-na.ssl-images-amazon.com/images/M/MV5BZjhkMDM4MWItZTVjOC00ZDRhLThmYTAtM2I5NzBmNmNlMzI1XkEyXkFqcGdeQXVyNDYyMDk5MTU@._V1_QL50_SY1000_CR0,0,679,1000_AL_.jpg",   # noqa
            "https://www.youtube.com/watch?v=zwhP5b4tD6g")

wall_e = media.Movie(
        "WALL E",
        "In the distant future,\
        a small waste-collecting robot inadvertently embarks on a space\
        journey that will ultimately decide the fate of mankind",
        "https://images-na.ssl-images-amazon.com/images/M/MV5BMjExMTg5OTU0NF5BMl5BanBnXkFtZTcwMjMxMzMzMw@@._V1_QL50_SY1000_CR0,0,674,1000_AL_.jpg",   # noqa
        "https://www.youtube.com/watch?v=alIq_wG9FNk")


movies_list = [
            shawshank,
            inception,
            saving_ryan,
            wall_e]

fresh_tomatoes.open_movies_page(movies_list)
