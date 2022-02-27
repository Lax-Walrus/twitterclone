function like(chirpsId) {
  const likeCount = document.getElementById(`likes-count-${chirpsId}`);
  const likeButton = document.getElementById(`like-button-${chirpsId}`);

  fetch(`/likechirp/${chirpsId}`, { method: "POST" })
    .then((res) => res.json())
    .then((data) => {
      likeCount.innerHTML = data["likes"];

      if (data["liked"]) {
        likeButton.className = "fas fa-thumbs-up";
      } else {
        likeButton.className = "far fa-thumbs-up";
      }
    })
    .catch((e) => alert("Could not like post."), console.log(e));
}
