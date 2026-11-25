import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { expect, test, vi } from "vitest";
import App from "./App";

vi.mock("./session", () => ({
  useSession: () => ({ user: null, loading: false, logout: vi.fn() }),
}));

test("shows navigation and recovery link for an unknown page", () => {
  render(
    <MemoryRouter initialEntries={["/unknown-page"]}>
      <App />
    </MemoryRouter>,
  );
  expect(
    screen.getByRole("heading", { name: "Страница не найдена" }),
  ).toBeVisible();
  expect(
    screen.getByRole("link", { name: "Вернуться к проектам" }),
  ).toHaveAttribute("href", "/");
  expect(screen.getByRole("link", { name: "Войти" })).toHaveAttribute(
    "href",
    "/login",
  );
});
