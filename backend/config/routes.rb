Rails.application.routes.draw do
  # 헬스 체크
  get "up" => "rails/health#show", as: :rails_health_check

  scope "/api", defaults: { format: :json } do
    resources :documents, only: %i[index show create] do
      resources :questions, only: %i[index create]
    end
  end
end
