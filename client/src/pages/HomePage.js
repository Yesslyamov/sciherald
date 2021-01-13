import { CircularProgress, Typography } from "@material-ui/core";
import React from "react";
import { useSelector } from "react-redux";
import { Article } from "../components/Article";
import parser from "html-react-parser";

export const HomePage = () => {
  const { articles, error, isLoading } = useSelector((state) => ({
    articles: state.articleList.articles,
    error: state.articleList.errors.articles,
    isLoading: state.articleList.loadings.articles,
  }));
  const circular = isLoading && <CircularProgress size={100} />;
  const articlesJSX =
    !isLoading &&
    !error &&
    articles.map((post, id) => {
      return (
        <Article
          id={post.id}
          title={post.name}
          description={parser(post.content.slice(0, 100))}
          key={post.name}
        />
      );
    });
  const errorJSX = error && <Typography variant="h6">{error}</Typography>;

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        minHeight: "80vh",
        alignItems: "center",
        width: "100%",
      }}
    >
      {circular}
      {errorJSX}
      {articlesJSX}
    </div>
  );
};
