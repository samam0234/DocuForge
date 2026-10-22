# 프론트엔드(Vue)에서 오는 교차 출처 요청만 허용한다.
Rails.application.config.middleware.insert_before 0, Rack::Cors do
  allow do
    origins ENV.fetch("FRONTEND_ORIGIN", "http://localhost:5173").split(",")

    resource "/api/*",
      headers: :any,
      methods: [ :get, :post, :options, :head ]
  end
end
